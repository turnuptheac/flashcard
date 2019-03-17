from datetime import timedelta
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import User

# Create your models here.

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 3600
SECONDS_IN_DAY = 86400

# Mapping of bucket number to time between reviews, in seconds
BUCKET_REVIEW_DELAY = {
    0: 0,
    1: 5,
    2: 25,
    3: 2 * SECONDS_IN_MINUTE,
    4: 10 * SECONDS_IN_MINUTE,
    5: SECONDS_IN_HOUR,
    6: 5 * SECONDS_IN_HOUR,
    7: SECONDS_IN_DAY,
    8: 5 * SECONDS_IN_DAY,
    9: 25 * SECONDS_IN_DAY,
    10: 121 * SECONDS_IN_DAY,  # 4 months
    11: -1,  # Never
}


class CardManager(models.Manager):
    """
    Custom model manager for the Card model

    We use this as it is the preferred way to add "table-level" functionality
    to a model.
    """
    def next_card(self, user):
        """
        Get the next card to be reviewed by a user

        Args:
            user: User object

        Returns:
            Card object or None
        """
        # Select any cards that aren't hard to remember (wrong_count >= 10) or
        # in bin 11 and select the first card after sorting by:
        # - bin (desc)
        # - created (desc)
        card = user.cards.filter(
            bucket__gte=0, bucket__lt=11, wrong_count__lt=10).order_by(
                '-bucket', '-created_at').first()
        return card

    def has_cards(self, user):
        """
        Determine if all a useer has cards

        Args:
            user: User object

        Returns:
            Boolean indicator
        """
        return user.cards.exists()

    def is_temporarily_done(self, user):
        """
        Determine if there are no words in bin 0, and all words still have still
        have positive counters.

        Args:
            user: User object

        Returns:
            Boolean indicator
        """
        has_cards = self.has_cards(user)
        is_permanently_done = self.is_permanently_done(user)
        bin0_empty = not user.cards.filter(bucket=0).exists()
        next_card = self.next_card(user)

        return (has_cards and bin0_empty and not is_permanently_done and
                next_card is None)

    def is_permanently_done(self, user):
        """
        Determine if all a user's cards are in the last bin or with the max
        number of failures.

        Args:
            user: User object

        Returns:
            Boolean indicator
        """
        useful_count = user.cards.filter(
            wrong_count__lt=10, bucket__lt=11).count()

        return self.has_cards(user) and useful_count == 0


class Card(models.Model):
    """
    Representation of a card
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        related_name='cards',
        on_delete=models.CASCADE,
        help_text=_('User that owns this card.'))

    word = models.CharField(
        _('word'),
        max_length=50,
        blank=False,
        help_text=_('Word to display on card.'))

    bucket = models.SmallIntegerField(
        _('bin'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(11)],
        help_text=_('Card play progress.'))

    MAX_WRONG_COUNT = 10
    wrong_count = models.SmallIntegerField(
        _('wrong count'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(MAX_WRONG_COUNT)],
        help_text=_('Lifetime wrong count.'))

    reviewed_at = models.DateTimeField(
        _('reviewed'),
        blank=True,
        null=True,
        help_text=_('Card last review date/time.'))

    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    objects = CardManager()

    def __str__(self):
        return self.word

    @property
    def is_hard_to_remember(self):
        return self.wrong_count >= self.MAX_WRONG_COUNT

    @property
    def time_to_next_review(self):
        duration = None
        delay = BUCKET_REVIEW_DELAY[self.bucket]
        if delay >= 0 and self.reviewed_at:
            now = timezone.now()
            review_at = self.reviewed_at + timedelta(seconds=delay)
            if review_at > now:
                duration = (review_at - now).seconds
            else:
                duration = 0
        return duration

    def success(self):
        self.reviewed_at = timezone.now()
        self.bucket = min(self.bucket + 1, 11)
        self.save()

    def failure(self):
        self.reviewed_at = timezone.now()
        self.wrong_count = min(self.wrong_count + 1, 10)
        self.bucket = 1
        self.save()
