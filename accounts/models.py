import uuid

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

# Create your models here.


# ------------------------------------------------------------------------------
# Custom User Model
# ------------------------------------------------------------------------------
class UserManager(BaseUserManager):
    """
    Custom UserManager for the custom AbstractUser
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        Args:
            email: user email
            password: user password
            **extra_fields: extra user model fields

        Returns:
            account.models.User object

        Raises:
            ValueError: email is not set
            ValidationError: invalid email address
        """
        # validate and normalize email
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email.lower())
        validators.validate_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        Args:
            email: user email
            password: user password
            **extra_fields: extra user model fields

        Returns:
            account.models.User: regular user

        Raises:
            ValueError: email is not set
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.

        Args:
            email: user email
            password: user password
            **extra_fields: extra user model fields

        Returns:
            account.models.User: admin user

        Raises:
            ValueError: email is not set
            ValueError: Superuser must have is_staff=True
            ValueError: Superuser must have is_superuser=True
            ValidationError: invalid email address
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_user_by_email(self, email, **extra_fields):
        """
        Get a user that already exists in our system or create a new, inactive
        `User` with a random password. This user has the provided email.
        This is the reason we have an `is_active` flag on the User object - so
        that users can be referenced in the system before they've signed up.

        Args:
            email: user email
            **extra_fields: extra user model fields

        Returns:
            User instance

        Raises:
            ValidationError: invalid email address
        """
        try:
            user = self.model.objects.get(email__iexact=email)
        except self.model.DoesNotExist:
            user = self._create_user(email, get_random_string(),
                                     is_active=False,
                                     **extra_fields)
        return user

    def get_by_natural_key(self, email):
        """
        Case-insensitive lookup which is necessary for case-insensitive
        authentication
        """
        return self.get(**{'email__iexact': email})


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with admin-compliant permissions.
    Django's default user doesn't work for us as we dont support username
    but instead email as the unique identifier field.

    Email and password are required. Other fields are optional.

    There is an interesting note about the context of 'is_active' in this model.
        When an app user invites contacts with given email addresses, not all
        those contacts will be registered on the service. These unregistered
        contacts will be represented as inactive users (is_active = False). If
        these contacts eventually sign up to the service all their data will
        simply be waiting for them.

    The following fields are inherited from the superclasses:
        * password
        * last_login
        * is_superuser
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        })

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    """
    Concrete User class. It's an extension of AbstractUser class.

    Email and password are required. Other fields are optional.
    """
    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        """
        Override the representation of users to use emails

        Args:
            None

        Returns:
            (str) user's email address
        """
        return self.email

    def get_full_name_initials(self):
        """
        Returns the initials from the full name
        """
        full_name = self.get_full_name()
        initials = '@'
        if full_name:
            first_words = full_name.split()[:2]
            first_letters = [w[0].upper() for w in first_words]
            initials = ''.join(first_letters)
        return initials
