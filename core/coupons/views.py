from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import View

from . import forms
from .services import CouponSystem


class ApplyCouponView(View):
    """ Make discount for cart final price using coupon """

    def post(self, request):
        form = forms.CouponApplyForm(request.POST)
        success = CouponSystem.coupon_activation(
            self=CouponSystem, request=request, form=form)
        if success:
            messages.add_message(request, messages.INFO,
                                 "Купон успішно застосовано!")
            return redirect('/cart/')
        else:
            messages.add_message(request, messages.INFO,
                                 "Вказаний купон недійсний!")
            return redirect('/cart/')
