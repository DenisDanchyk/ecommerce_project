from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from coupons.models import Coupon
from accounts.models import *


class CartProduct(models.Model):
    """ Product model for cart """

    user = models.ForeignKey(
        'accounts.UserBase', on_delete=models.CASCADE, verbose_name='Покупець')
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE,
                             verbose_name='Корзина', related_name='related_products')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    user_size_choice = models.CharField(
        max_length=255, null=True, verbose_name='Вибраний користовачем розмір')

    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, verbose_name='Ціна')

    def save(self, *args, **kwargs):
        if self.content_object.discount_price:
            self.final_price = self.quantity * self.content_object.discount_price
        else:
            self.final_price = self.quantity * self.content_object.price
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__._meta.model_name

    def __str__(self):
        return f'Продукт (для корзини) для покупця {self.user}'

    class Meta:
        verbose_name = 'Продукти для корзини'
        verbose_name_plural = 'Продукт для корзини'


class Cart(models.Model):
    """ Cart model """

    owner = models.ForeignKey(
        'accounts.UserBase', on_delete=models.CASCADE, verbose_name='Власник', null=True)
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart', verbose_name="Продукти")
    total_products = models.PositiveIntegerField(
        default=0, verbose_name='Кількість продуктів')
    final_price = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, verbose_name='Фінальна ціна')
    in_order = models.BooleanField(default=False, verbose_name="В обробці")
    for_anonymos_user = models.BooleanField(
        default=False, verbose_name="Для не авторизованих користувачів")
    coupons = models.ManyToManyField(Coupon, related_name='related_coupons')

    def __str__(self):
        return f'Корзина для покупця {self.owner}'

    class Meta:
        verbose_name_plural = 'Корзина'
        verbose_name_plural = 'Корзини'
