from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=[
            'username',
            'first_name',
            'last_name',
            'password',
            'is_staff',
            'role'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
