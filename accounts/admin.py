from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """
    Custom version of the ModelAdmin associated with the User model. It is
    modified to work with the custom User model

    A custom user model requires using a custom form and add_form
    """
    # These fields to be used in displaying the User model. These override the
    # definitions on the base UserAdmin that reference specific fields on
    # auth.User
    list_display = ('email', 'first_name', 'last_name',
                    'date_joined', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',
                                           'updated_at')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )
    form = UserChangeForm
    add_form = UserCreationForm

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('id', 'last_login', 'date_joined', 'updated_at',)
