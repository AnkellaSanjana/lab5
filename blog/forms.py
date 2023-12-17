from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import BlogPost, CustomUser


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content"]


class LoginForm(AuthenticationForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "bio",
            "profile_picture",
        ]
