from decimal import Decimal
from django.utils import timezone

from cart.services import CustomerCart

from .models import Coupon


def coupon_activation(request, form):
    """ Coupon activation """

    if form.is_valid():
        now = timezone.now()
        code = form.cleaned_data['code']
        try:
            coupon = _get_coupon(code=code, now=now)
            cart = CustomerCart.get_customer_cart(request)
            _make_coupon_discount(cart=cart, coupon=coupon)
            CustomerCart._save_cart(cart=cart)
            return True
        except Coupon.DoesNotExist:
            return False


def _get_coupon(code, now):
    """ Get coupon """

    coupon = Coupon.objects.get(code=code,
                                valid_from__lte=now,
                                valid_to__gte=now,
                                active=True)
    return coupon


def _make_coupon_discount(cart, coupon):
    """ Make discount for cart final price using coupon """

    cart.final_price = (
        coupon.discount / Decimal(100)) * cart.final_price
