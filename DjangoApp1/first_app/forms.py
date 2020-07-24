from django import forms
# from first_app.models import Register
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm


# class FormName(forms.ModelForm):
#     # first_name = forms.CharField()
#     # last_name = forms.CharField()
#     # email = forms.EmailField()
#
#     class Meta():
#         model = Register
#         fields = '__all__'


# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta():
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password')
#

class UserForm(UserCreationForm):
    username = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', ]


class PasswordReset(PasswordResetForm):
    username = forms.EmailField()

    class Meta:
        model = User
        fields = ['username']

class SetNewPassword(forms.Form):
    new_password1 = forms.CharField(
        label= ("New password"),
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label= ("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )
