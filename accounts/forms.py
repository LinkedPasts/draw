from django import forms
from django.contrib.auth.models import User, Group
from django.db import models

from accounts.models import Profile

class UserModelForm(forms.ModelForm):
#
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name',)
        exclude = ('password',)
        widgets = {'email': forms.EmailInput(attrs={'size':60})}
#
class ProfileModelForm(forms.ModelForm):
#
    class Meta:
        model = Profile
        fields = ('name','affiliation','web_page','user_type')
        widgets = {
            'name': forms.TextInput(attrs={'size': 60}),
            'affiliation': forms.TextInput(attrs={'size': 60}),
            'web_page': forms.TextInput(attrs={'size': 60}),
            'password': forms.PasswordInput(attrs={'size': 60}),
        }
