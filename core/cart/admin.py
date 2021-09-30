from django.contrib import admin
from .models import CartProduct, Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['owner', 'final_price', 'in_order', 'for_anonymos_user']


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart', 'content_object', 'final_price']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
