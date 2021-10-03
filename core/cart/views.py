from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages

from django.views.generic import View
from store.services import ProductSystem

from coupons.forms import CouponApplyForm

from .mixins import CartMixin
from .services import CustomerCart


class AddToCartView(CartMixin, View):
    """ Add product to customer cart """

    def post(self, request, **kwargs):
        if self.cart.for_anonymos_user:
            messages.add_message(request, messages.SUCCESS,
                                 "Добавлення товару до корзини доступно лише авторизованим користувачам!")
            return redirect('store:products_list')

        cart_product, create = CustomerCart.get_or_create_cart_product(
            self=ProductSystem,
            cart=self.cart, kwargs=kwargs)
        CustomerCart.add_product_to_cart(self=CustomerCart, request=request,
                                         cart_product=cart_product, create=create)
        self.cart.save()

        CustomerCart.recal_total_products_in_cart(
            self=CustomerCart, cart=self.cart)
        messages.add_message(request, messages.SUCCESS,
                             "Товар успішно додано в корзину")
        return redirect('store:products_list')


class DeleteFromCartView(CartMixin, View):
    """ Delete product from customer cart """

    def get(self, request, **kwargs):

        cart_product = CustomerCart.get_cart_product(
            self=ProductSystem,
            cart=self.cart, kwargs=kwargs
        )

        CustomerCart.remove_product_from_cart(
            self=CustomerCart, cart_product=cart_product)
        CustomerCart.recal_total_products_in_cart(
            self=CustomerCart, cart=self.cart)
        messages.add_message(request, messages.WARNING,
                             "Товар успішно видалено з корзини")
        return HttpResponseRedirect('/cart/')


class ChangeQuantityView(CartMixin, View):
    """ Change product quantity in customer cart """

    def post(self, request, **kwargs):
        cart_product = CustomerCart.get_cart_product(
            self=ProductSystem, cart=self.cart, kwargs=kwargs
        )

        CustomerCart.change_product_quantity(
            self=CustomerCart, request=request, cart_product=cart_product)
        CustomerCart.recal_total_products_in_cart(
            self=CustomerCart, cart=self.cart)
        messages.add_message(request, messages.INFO,
                             "Кількість товару успішно змінено!")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    """ Show customer cart page """

    def get(self, request):
        coupon_form = CouponApplyForm()
        return render(request, 'cart/cart_page.html', {'cart': self.cart, 'coupon_form': coupon_form})
