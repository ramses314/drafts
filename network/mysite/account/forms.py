from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput

from .models import Profile



class LoginForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='pass', widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='pass2', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {
            'username' : TextInput(attrs={'placeholder' : 'Никнейм'}),
            'first_name': TextInput(attrs={'placeholder': 'Имя'}),
            'email': EmailInput(attrs={'placeholder': 'Почты'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('ne sovpadayut')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name' : forms.TextInput(attrs={'placeholder' : 'имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'почта'})
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_birth', 'photo']

        widgets = {
            'date_birth': forms.TextInput(attrs={'placeholder': 'дата рождения'}),
            'photo': forms.FileInput(attrs={'placeholder': ''}),

        }

