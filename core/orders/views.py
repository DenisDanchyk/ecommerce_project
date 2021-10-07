from django.shortcuts import render, redirect
from django.views.generic import View

from cart.mixins import CartMixin
from cart.services import CartSystem
from coupons.services import CouponSystem


from .services import OrderSystem
from .forms import OrderForm


class CheckoutView(View):
    """ Show checkout page """

    def get(self, request):
        form = OrderForm()
        cart = CartSystem.get_customer_cart(request)
        cart_products = CartSystem.get_cart_products(cart=cart)
        coupons = CouponSystem.get_coupons_applied_to_cart(cart=cart)

        return render(request, 'orders/checkout.html', {'form': form,
                                                        'cart_products': cart_products,
                                                        'cart': cart,
                                                        'coupons': coupons})


class CreateOrderView(CartMixin, View):
    """ Create order """

    def post(self, request):
        form = OrderForm(request.POST)
        form, success = OrderSystem.create_order(
            self=OrderSystem, form=form, cart=self.cart)
        if form.errors:
            cart = CartSystem.get_customer_cart(request)
            cart_products = CartSystem.get_cart_products(cart=cart)
            return render(request, 'orders/checkout.html', {'form': form,
                                                            'cart_products': cart_products,
                                                            'cart': cart})
        if success:
            return render(request, 'orders/order_valid.html')
        else:
            return redirect('/order/invalid_order/')
