from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.core.mail import send_mail

from phonenumber_field.modelfields import PhoneNumberField

from orders.models import *


class CustomAccountManager(BaseUserManager):
    """ Custom create user account """

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Адмін повинен мати параметр is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Адмін повинен мати параметр is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **other_fields)

    def create_user(self, email, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError('Ви повинні вказати Електронну адресу')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """
    email = models.EmailField(unique=True, verbose_name="Електронна адреса")
    phone = PhoneNumberField(unique=True, blank=True,
                             verbose_name="Номер телефону")

    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="Ім'я")
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name="Фамілія")

    city = models.CharField(max_length=150, blank=True, verbose_name="Місто")

    orders = models.ManyToManyField(
        'orders.Order', related_name="related_order", verbose_name="Замовлення покупця", blank=True)

    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Акаунт'
        verbose_name_plural = 'Акаунти'

    def __str__(self):
        return self.email

    # Send email token for ragistration
    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )
