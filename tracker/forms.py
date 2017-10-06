from django import forms
from django.contrib.auth.models import User

from .models import Objective


def get_user_by_email_or_username(username_email):
    try:
        user = User.objects.get(email=username_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(username=username_email)
        except User.DoesNotExist:
            user = None

    return user


class SigninForm(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username or email address",
            }
        )
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )

    def clean(self):
        cleaned_data = super(SigninForm, self).clean()
        username_email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = get_user_by_email_or_username(username_email)

        if user is None:
            raise forms.ValidationError("No user was found with the given username/email address.")
        elif not user.check_password(password):
            raise forms.ValidationError("Incorrect password.")


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        )
    )
    email = forms.CharField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
            }
        )
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )
    confirm_password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
            }
        )
    )

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")


class TimeEntryForm(forms.Form):
    objective = forms.ModelChoiceField(
        queryset=Objective.objects,
        empty_label="None",
        widget=forms.Select(
            attrs={
                "class": "form-control custom-select",
            }
        )
    )
    explanation = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Explanation",
            }
        )
    )
    effort = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.5",
                "min": "0",
                "max": "24"
            }
        )
    )
