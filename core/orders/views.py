from django.shortcuts import render
from django.views.generic import View

from cart.mixins import CartMixin
from cart.services import CustomerCart

from .services import OrderSystem
from .forms import OrderForm


class CheckoutView(View):
    """ Shot checkout page """

    def get(self, request):
        form = OrderForm(request.POST)
        cart = CustomerCart.get_customer_cart(request)
        cart_products = CustomerCart.get_cart_products(cart=cart)

        return render(request, 'orders/checkout.html', {'form': form,
                                                        'cart_products': cart_products,
                                                        'cart': cart})


class CreateOrderView(CartMixin, View):
    """ Create order """

    def post(self, request):
        form = OrderForm(request.POST)
        success = OrderSystem.create_order(self=OrderSystem, form=form,
                                           cart=self.cart)
        if success:
            return render(request, 'orders/order_valid.html')
        else:
            return render(request, 'orders/order_invalid.html')
