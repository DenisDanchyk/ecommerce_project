from django import forms
from django.contrib.auth.forms import AuthenticationForm

from phonenumber_field.formfields import PhoneNumberField

from .models import UserBase


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField()  # Email
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': '+380(11)9999999', 'maxlength': 15}))
    phone.error_messages['invalid'] = 'Введіть коректний номер телефону (наприклад, +380(11)9999999).'

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        widgets = {
            'email': forms.TextInput(
                attrs={'placeholder': 'example@gmail.com', 'maxlength': 30}
            ),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Тест', 'maxlength': 30}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Тестов', 'maxlength': 30}
            ),
        }
        fields = ('email', 'first_name', 'last_name', 'city',)

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Пароль не збігається.")
        return self.cleaned_data['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        e = UserBase.objects.filter(email=email)
        if e.count():
            raise forms.ValidationError(
                "Акаунт з таким електронним адресом вже існує!")
        return email





class EditPersonalInformationForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ('email', 'first_name', 'last_name', 'city', 'phone')
