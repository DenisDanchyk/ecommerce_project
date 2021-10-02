from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string

from django.contrib.auth import login

from cart.models import Cart

from .models import UserBase
from .token import account_activation_token


class CustomerAccount:
    """ CustomerAccount class for manipulate with customer account  """

    def registration(self, request, form):
        """ Registration customer account """

        if form.is_valid():
            user = self._create_account_data(form=form)
            self._activation_account_using_email(request, user=user)

    def activation_customer_account(request, user):
        """ Activation customer account """

        user.is_active = True
        user.save()
        Cart.objects.create(owner=user)
        login(request, user)

    def get_user_uid(uidb64):
        """ Get customer account using  uidb64 """

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
        return user

    def get_customer_account(request):
        """ Get customer account """

        customer = UserBase.objects.get(email=request.user)
        return customer

    def validate_personal_edit_data(form):
        """ Validate edit data information """

        if form.is_valid():
            form.save()
        return form

    def _create_account_data(form):
        """ Create user instance """

        user = form.save(commit=False)

        user.set_password(form.cleaned_data['password'])
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.city = form.cleaned_data['city']
        user.phone = form.cleaned_data['phone']
        user.is_active = False

        user.save()
        return user

    def _activation_account_using_email(request, user):
        """ Send email with token to customer """

        current_site = get_current_site(request)
        subject = 'Активація акаунту'
        message = render_to_string('accounts/registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uidb': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject=subject, message=message)
