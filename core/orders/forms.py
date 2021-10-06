from django import forms
from phonenumber_field.formfields import PhoneNumberField

from orders.models import Order


class OrderForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': '+380(11)9999999', 'maxlength': 16}))
    phone.error_messages[
        'invalid'] = 'Введіть коректний номер телефону (наприклад, +380(11)9999999).'

    class Meta:
        model = Order
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': "Ім'я", 'maxlenght': 30}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Фамілія', 'maxlenght': 30}
            ),
            'email': forms.TextInput(
                attrs={'placeholder': 'Email', 'maxlenght': 50}
            ),
            'post_office': forms.TextInput(
                attrs={'placeholder': 'Номер пошти', 'maxlenght': 4}
            ),
            'comment': forms.TextInput(
                attrs={
                    'placeholder': 'Вкажіть додатвоку інформацію, якщо це необхідно', 'maxlenght': 250}
            ),
        }
        fields = ('first_name', 'last_name', 'phone',
                  'email', 'city', 'post_office', 'comment')

    def clean_post_office(self):
        post_office = self.cleaned_data['post_office']
        for i in post_office:
            try:
                int(i)
            except ValueError:
                raise forms.ValidationError(
                    "Номер пошти повинен складатися лише з цифр!")
        return post_office

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        for i in first_name:
            try:
                int(i)
                raise forms.ValidationError(
                    "В імені не повинно бути цифр!")
            except ValueError:
                pass
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        for i in last_name:
            try:
                int(i)
                raise forms.ValidationError(
                    "В фімілії не повинно бути цифр!")
            except ValueError:
                pass
        return last_name
