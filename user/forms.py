from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="ইমেইল এড্রেস")
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        widgets = {
            'bio':forms.Textarea(attrs={'rows':3, 'placeholder':'Write somethings yourself '})
        }