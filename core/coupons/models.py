from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """ Coupon model """

    code = models.CharField(max_length=50, verbose_name="Промокод")
    valid_from = models.DateTimeField(verbose_name="Дійсний з")
    valid_to = models.DateTimeField(verbose_name="Дійсний до")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Процент знижки")
    active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купони'
