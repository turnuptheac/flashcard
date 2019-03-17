from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cards.models import Card

# Register your models here.


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """
    Representation of the Card model in the admin interface.
    """
    list_display = ('word', 'bucket', 'wrong_count',
                    'reviewed_at', 'created_at')
    list_filter = ('bucket',)
    fieldsets = (
        (None, {'fields': ('id', 'user')}),
        (_('Summary'), {'fields': ('word',)}),
        (_('Review'), {'fields': ('bucket', 'wrong_count', 'reviewed_at',
                                  'time_to_next_review',
                                  'is_hard_to_remember',)}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    search_fields = ('word',)
    readonly_fields = ('id', 'time_to_next_review', 'is_hard_to_remember',
                       'created_at', 'updated_at')
    ordering = ('-created_at',)

    def is_hard_to_remember(self, obj):
        return obj.is_hard_to_remember
    is_hard_to_remember.boolean = True
