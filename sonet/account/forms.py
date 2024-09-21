from django import forms
from django.contrib.auth.models import User
from .models import Bio

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class BioUpdateForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ['bio']


class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Bio  # You can replace this with your actual user model if needed
        fields = ['profile_picture'] 