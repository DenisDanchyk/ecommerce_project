from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import View

from . import forms
from .services import coupon_activation


class ApplyCouponView(View):
    """ Make discount for cart final price using coupon """

    def post(self, request):
        form = forms.CouponApplyForm(request.POST)
        success = coupon_activation(request, form=form)
        if success:
            messages.add_message(request, messages.INFO,
                                 "Купон успішно застосовано!")
            return redirect('/cart/')
        else:
            messages.add_message(request, messages.INFO,
                                 "Вказаний купон недійсний!")
            return redirect('/cart/')
