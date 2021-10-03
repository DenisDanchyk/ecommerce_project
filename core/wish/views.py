from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from store.services import ProductSystem

from .mixins import WishMixin
from .services import (get_or_create_wish_product, add_product_to_wish,
                       save_wish, get_wish_product, remove_wish_product)


class AddToWishView(WishMixin, View):
    """ Add product to wish """

    def get(self, request, **kwargs):
        if self.wish.for_anonymos_user:
            messages.add_message(request, messages.SUCCESS,
                                 "Добавлення товару до списку бажаних товарів доступно лише авторизованим користувачам!")
            return redirect('store:products_list')
        wish_product, create = get_or_create_wish_product(
            self=ProductSystem, wish=self.wish, kwargs=kwargs
        )
        if create:
            add_product_to_wish(wish=self.wish, wish_product=wish_product)
            messages.add_message(
                request, messages.SUCCESS, "Товар успішно даданий у ваш список бажаних товарів")
        else:
            messages.add_message(
                request, messages.SUCCESS, "Товар уже знаходиться у вашому списку бажаних товарів")

        save_wish(wish=self.wish)
        return redirect('store:products_list')


class DeleteWishView(WishMixin, View):
    """ Delete product from wish """

    def get(self, request, kwargs):
        wish_product = get_wish_product(
            self=ProductSystem,
            wish=self.wish, **kwargs
        )
        remove_wish_product(wish=self.wish, wish_product=wish_product)
        save_wish(wish=self.wish)
        messages.add_message(request, messages.WARNING,
                             "Товар успішно видалено з списку бажаних товарів")
        return HttpResponseRedirect('/wish/')


class WishView(WishMixin, View):
    """ Show wish page """

    def get(self, request):
        return render(request, 'wish/wish_page.html', {'wish': self.wish})
