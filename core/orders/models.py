from django.db import models
from django.utils import timezone

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from cart.models import *
from accounts.models import *


class OrderItem(models.Model):
    """ Item model for order """

    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, verbose_name="Замовлення")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    """ Order model """

    STATUS_CHOICES = (
        ("STATUS_NEW", "Нове замовлення"),
        ("STATUS_IN_PROCESS", "Замовлення в процесі обробки"),
        ("STATUS_READY", "Замовлення готове"),
        ("STATUS_COMPLETED", "Замовлення виконане"),
    )

    BYING_TYPE = (
        ("BYING_TYPE_SELF", "Самовивіз"),
        ("BYING_TYPE_DELIVERY", "Доставка"),
    )

    customer = models.ForeignKey(
        'accounts.UserBase', on_delete=models.CASCADE, related_name="related_orders", verbose_name='Покупець')
    cart = models.ForeignKey(
        'cart.Cart', on_delete=models.CASCADE, verbose_name="Корзина", null=True
    )
    first_name = models.CharField(max_length=255,  verbose_name="Ім'я")
    last_name = models.CharField(max_length=255,  verbose_name="Фамілія")
    phone = models.CharField(max_length=255,  verbose_name="Номер телефону")
    city = models.CharField(max_length=255, verbose_name="Місто")
    post_office = models.CharField(
        max_length=255, verbose_name="Вдділення пошти")
    email = models.EmailField()
    comment = models.TextField(
        null=True, blank=True, verbose_name="Комментар до замовлення")

    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][1], verbose_name="Статус")

    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення замовлення")
    order_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата доставки товару покупцю")

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return str(self.id)
