from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

class registeration_form(UserCreationForm):

    password2 = forms.CharField(label="Confirm Password :", widget=forms.PasswordInput)
    first_name = forms.CharField(label="First name :",required=True)
    last_name = forms.CharField(label="Last name :",required=True)
    email = forms.EmailField(label="E-mail ID :",required=True)
    username = forms.CharField(label="Username :", required=True)
    password1 = forms.CharField(label="Password :", widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username' ,'email','password1','password2']

class login_form(AuthenticationForm):

    username = forms.CharField(label="Username :" , required=True)
    password = forms.CharField(label="Password :" ,widget=forms.PasswordInput , required=True)
    email = forms.EmailField(label="E-mail ID :" ,required=True)

class change_password_form(PasswordChangeForm):

    old_password = forms.CharField( label="Old Password ",widget=forms.PasswordInput , required=True)
    new_password1 = forms.CharField(label="New Password ", widget=forms.PasswordInput , required=True)
    new_password2 = forms.CharField(label="Confirm New Password ", widget=forms.PasswordInput , required=True)

class change_email_form(forms.ModelForm):

    email = forms.EmailField(label="Enter New Email ",required=True)

    class Meta:
        model = User
        fields = ['email']