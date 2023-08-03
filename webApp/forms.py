from django import forms
from django.contrib.auth.forms import UserCreationForm


class CreateTag(forms.Form):
    symbol = forms.CharField(label="Symbols of the tag", initial="")


class CustomUserCreationForm(UserCreationForm):
    pass
