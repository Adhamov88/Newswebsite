from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from accounts.models import Profile


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Parol',widget=forms.PasswordInput)
    password_2=forms.CharField(label='Parolni almashtring',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','email',]
    def clean_password_2(self):
        data=self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError('Parol bir biriga teng emas')
        return data['password_2']
class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['date_of_birth','photo']
class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model=User
        fields=['old_password','password1','password2']


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'photo','date_of_birth'
