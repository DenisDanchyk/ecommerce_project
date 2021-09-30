from django.contrib import admin
from .models import Wish, WishProduct


class WishAdmin(admin.ModelAdmin):
    list_display = ['owner', 'for_anonymos_user']


class WishProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'wish', 'content_object']


admin.site.register(Wish, WishAdmin)
admin.site.register(WishProduct, WishProductAdmin)
