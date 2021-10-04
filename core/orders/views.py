from django.shortcuts import render
from django.views.generic import View

from cart.mixins import CartMixin
from cart.services import CartSystem

from .services import OrderSystem
from .forms import OrderForm


class CheckoutView(View):
    """ Shot checkout page """

    def get(self, request):
        form = OrderForm()
        cart = CartSystem.get_customer_cart(request)
        cart_products = CartSystem.get_cart_products(cart=cart)

        return render(request, 'orders/checkout.html', {'form': form,
                                                        'cart_products': cart_products,
                                                        'cart': cart})


class CreateOrderView(CartMixin, View):
    """ Create order """

    def post(self, request):
        form = OrderForm(request.POST)
        form = OrderSystem.create_order(self=OrderSystem, form=form,
                                        cart=self.cart)
        cart = CartSystem.get_customer_cart(request)
        cart_products = CartSystem.get_cart_products(cart=cart)
        if form.errors:
            return render(request, 'orders/checkout.html', {'form': form,
                                                            'cart_products': cart_products,
                                                            'cart': cart})
        else:
            return render(request, 'orders/order_valid.html')
