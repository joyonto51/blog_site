from django import forms
from django.forms import models

from accounts.models import User, UserInfo
from django.core.exceptions import ValidationError


class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30)
    re_password = forms.CharField(max_length=30)
    #
    # def __init__(self, **kwargs):
    #     super(SignUpForm, self).__init__()
    #
    #     self.email = kwargs['email']
    #     self.password = kwargs['password']
    #     self.re_password = kwargs['re_password']

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        re_password = self.cleaned_data.pop('re_password')

        if password != re_password:
            raise ValidationError("Password doesn't match")

        if User.objects.filter(email=email).exists():
            raise ValidationError("The email already exist")

        else:
            self.cleaned_data['username'] = email

        return self.cleaned_data


class UserForm(models.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UserInfoForm(models.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = UserInfo
        fields = ['image', 'phone', 'profession', 'address']
