"""
When using a custom user model some built-in auth forms must be rewritten,
UserCreationForm and UserChangeForm
"""

from django.contrib.auth import forms as auth_forms

from accounts.models import User


class UserCreationForm(auth_forms.UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.

    This overrides the Django form to use the custom User model and replace the
    username field with an email field.
    """
    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(auth_forms.UserChangeForm):
    """
    A form for updating users. Includes all the fields on the user, but replaces
    the password field with admin's password hash display field.

    This overrides the Django form to use the custom User model.
    """
    class Meta:
        model = User
        fields = '__all__'
