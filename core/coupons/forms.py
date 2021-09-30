from django import forms
from .models import Coupon

class CouponApplyForm(forms.ModelForm):
    class Meta:
        model = Coupon
        
        widgets = {
            'code': forms.TextInput(
                    attrs={'placeholder': 'Промокод'}
                ),
        }
        fields = ['code',]