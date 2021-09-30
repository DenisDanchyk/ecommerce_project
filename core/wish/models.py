from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from accounts.models import *


class WishProduct(models.Model):
    """ Product model for wish """

    user = models.ForeignKey(
        'accounts.UserBase', on_delete=models.CASCADE, verbose_name='Покупець')
    wish = models.ForeignKey('Wish', on_delete=models.CASCADE,
                             verbose_name='Список бажаних товарів', related_name='related_wishproducts')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Бажаний товар (для списку бажаних товарів) для покупця {self.user}'

    class Meta:
        verbose_name = 'Бажаний товар'
        verbose_name_plural = 'Бажані товари'


class Wish(models.Model):
    """ Wish model """

    owner = models.ForeignKey(
        'accounts.UserBase', on_delete=models.CASCADE, verbose_name='Власник', null=True)
    products = models.ManyToManyField(
        WishProduct, blank=True, related_name='related_wish', verbose_name='Продукти')
    for_anonymos_user = models.BooleanField(
        default=False, verbose_name='Для анонімних користувачів')

    class Meta:
        verbose_name = 'Список бажаних товарів'
        verbose_name_plural = 'Списки бажаних товарів'
