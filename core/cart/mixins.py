
from django.views.generic import View

from cart.services import CartSystem


class CartMixin(View):
    """ Get or create cart for customer """

    def dispatch(self, request, *args, **kwargs):
        cart = CartSystem.get_or_create_customer_cart(
            self=CartSystem, request=request)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
