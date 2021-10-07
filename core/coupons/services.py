from decimal import Decimal
from django.utils import timezone

from cart.services import CartSystem

from .models import Coupon


class CouponSystem:
    """ Manipulate with coupon system  """

    def coupon_activation(self, request, form):
        """ Coupon activation """

        if form.is_valid():
            now = timezone.now()
            code = form.cleaned_data['code']
            try:
                coupon = self._get_coupon(code=code, now=now)
                cart = CartSystem.get_customer_cart(request)
                if self._check_if_coupon_is_applied(cart=cart, coupon=coupon):
                    self._make_coupon_discount(cart=cart, coupon=coupon)
                    CartSystem._add_coupon_to_cart(cart=cart, coupon=coupon)
                    self._add_cart_to_coupon(cart=cart, coupon=coupon)
                    CartSystem.save_cart(cart=cart)
                    return True
            except Coupon.DoesNotExist:
                return False

    def get_coupons_applied_to_cart(cart):
        """ Get coupons that applied to cart """

        coupons = cart.coupons.all
        return coupons

    def _add_cart_to_coupon(cart, coupon):
        """ Add (tie) the cart to the coupon """

        coupon.applied_to.add(cart)

    def _check_if_coupon_is_applied(cart, coupon):
        """ Check if the coupon is already applied """

        if not cart.coupons.filter(code=coupon.code).first():
            return True
        else:
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

        cart.final_price = cart.final_price - ((
            coupon.discount / Decimal(100)) * cart.final_price)
