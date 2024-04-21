from django import forms
from .models import Website, CustomUser
from django.contrib.auth.forms import UserCreationForm
class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['url']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')