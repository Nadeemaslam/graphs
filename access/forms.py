from django import forms 
from django.contrib.auth.models import User
from api import UserInstanceResource
from models import USER_ROLE


class LoginForm(forms.Form):
    """Login Form for all users"""

    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Email',
               'class': 'login-user-input',
               'id': 'email',
               'onfocus': "this.placeholder = ''",
               'onblur': "this.placeholder = 'Email'"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'password',
               'class': 'login-pass-input',
               'id': 'password',
               'onfocus': "this.placeholder = ''",
               'onblur': "this.placeholder = 'password'"}))


class SignUpForm(forms.Form):
    '''file are uploaded using this form'''

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '',
                                      'class': 'form-control',
                                      'id': 'email'}),
        required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '',
                                                              'class': 'form-control',
                                                              'id': 'email'}),
                                required=True)
    
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email',
                                      'class': 'form-control',
                                      'id': 'email'}),
        required=True)
    password = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                          'class': "form-control"})
    )
    password_confirm = forms.CharField(
        label=("Password (again)"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-type Password',
                                          'class': "form-control"}))

    user_type = forms.ChoiceField(choices = USER_ROLE, required=True)


    def clean_email(self):
        email = self.cleaned_data["email"]
        user = UserInstanceResource()._filter(email=email)
        if user:
            raise forms.ValidationError(
                ("A user is registered with this email address."))
        return email

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data[
                "password_confirm"]:
                raise forms.ValidationError(
                    ("You must type the same password each time."))
        return self.cleaned_data

class UserEditForm(forms.Form):
    '''file are uploaded using this form'''
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email',
                                      'class': 'form-control',
                                      'id': 'email'}),
        required=True)

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '',
                                      'class': 'form-control',
                                      'id': 'email'}),
        required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '',
                                                              'class': 'form-control',
                                                              'id': 'email'}),
                                required=True)
    def clean_email(self):
        email = self.cleaned_data["email"]
        user = UserInstanceResource()._filter(email=email)
        if user:
            raise forms.ValidationError(
                ("A user is registered with this email address."))
        return email
    