from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from store.services import ProductSystem

from .mixins import WishMixin
from .services import WishSystem


class AddToWishView(WishMixin, View):
    """ Add product to wish """

    def get(self, request, **kwargs):
        if self.wish.for_anonymos_user:
            messages.add_message(request, messages.SUCCESS,
                                 "Добавлення товару до списку бажаних товарів доступно лише авторизованим користувачам!")
            return redirect('store:products_list')
        wish_product, create = WishSystem.get_or_create_wish_product(
            self=ProductSystem, wish=self.wish, kwargs=kwargs
        )
        if create:
            WishSystem.add_product_to_wish(wish_product=wish_product)
            messages.add_message(
                request, messages.SUCCESS, "Товар успішно даданий у ваш список бажаних товарів")
        else:
            messages.add_message(
                request, messages.SUCCESS, "Товар уже знаходиться у вашому списку бажаних товарів")

        WishSystem.save_wish(wish=self.wish)
        return redirect('store:products_list')


class DeleteWishView(WishMixin, View):
    """ Delete product from wish """

    def get(self, request, **kwargs):
        wish_product = WishSystem.get_wish_product(
            self=ProductSystem,
            wish=self.wish, kwargs=kwargs
        )
        WishSystem.remove_wish_product(wish_product=wish_product)
        WishSystem.save_wish(wish=self.wish)
        messages.add_message(request, messages.WARNING,
                             "Товар успішно видалено з списку бажаних товарів")
        return HttpResponseRedirect('/wish/')


class WishView(WishMixin, View):
    """ Show wish page """

    def get(self, request):
        return render(request, 'wish/wish_page.html', {'wish': self.wish})
