from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': "Ім'я", 'maxlenght':30}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder':'Фамілія', 'maxlenght':30}
            ),
            'phone': forms.TextInput(
                attrs={'placeholder':'Номер телефону', 'maxlenght':13}
            ),
            'email': forms.TextInput(
                attrs={'placeholder':'Email', 'maxlenght':50}
            ),
            'city': forms.TextInput(
                attrs={'placeholder':'Місто', 'maxlenght':30}
            ),
            'post_office': forms.TextInput(
                attrs={'placeholder':'Номер пошти', 'maxlenght':4}
            ),
            'comment': forms.TextInput(
                attrs={'placeholder':'Вкажіть додатвоку інформацію, якщо це необхідно', 'maxlenght':250}
            ),
        }
        fields = ('first_name', 'last_name', 'phone', 'email','city', 'post_office', 'comment')
