from django import forms
# from first_app.models import Register
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
