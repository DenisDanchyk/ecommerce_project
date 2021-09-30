from django.shortcuts import render

from django.views.generic import View

from cart.mixins import CartMixin
from accounts.services import get_customer_account
from cart.services import get_cart_products, get_customer_cart

from .services import create_order
from .forms import OrderForm


class CheckoutView(View):
    """ Shot checkout page """

    def get(self, request):
        form = OrderForm(request.POST)
        cart = get_customer_cart(request)
        cart_products = get_cart_products(cart=cart)

        return render(request, 'orders/checkout.html', {'form': form,
                                                        'cart_products': cart_products,
                                                        'cart': cart})


class CreateOrderView(CartMixin, View):
    """ Create order """

    def post(self, request):
        form = OrderForm(request.POST)
        customer = get_customer_account(request)
        success = create_order(form=form, cart=self.cart, customer=customer)
        if success:
            return render(request, 'orders/order_valid.html')
        else:
            return render(request, 'orders/order_invalid.html')
