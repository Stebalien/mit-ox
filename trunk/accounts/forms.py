from django import forms
import tagging.forms
from accounts.models import *
from exchange.index import complete_indexer
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        exclude = 'user'
        model = Profile

class UserForm(forms.ModelForm):
    class Meta:
        fields = ('first_name', 'last_name')
        model = User
