
from django.views.generic import View

from cart.services import get_or_create_customer_cart


class CartMixin(View):
    """ Get or create cart for customer """

    def dispatch(self, request, *args, **kwargs):
        cart = get_or_create_customer_cart(request)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
