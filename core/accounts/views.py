
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.base import View

from .forms import RegistrationForm, EditPersonalInformationForm
from .token import account_activation_token
from .services import AccountSystem


from orders.services import  OrderSystem
from cart.services import CartSystem


@method_decorator(login_required, name='dispatch')
class AccountPage(View):
    """ Show customer account page """

    def get(self, request):
        customer = AccountSystem.get_customer_account(request)
        return render(request, 'accounts/account.html', {'customer': customer, })


@method_decorator(login_required, name='dispatch')
class AccountPersonalInformation(View):
    """ Show customer personal information page """

    def get(self, request):
        customer = AccountSystem.get_customer_account(request)
        return render(request, 'accounts/account_personal_information.html', {'customer': customer})


class EditPersonalInformation(View):
    """ Edit customer personal information """

    def post(self, request):
        user_edit_form = EditPersonalInformationForm(
            request.POST, instance=request.user)
        AccountSystem.validate_personal_edit_data(form=user_edit_form)
        return redirect('/account/personal_information/')

    def get(self, request):
        user_edit_form = EditPersonalInformationForm(instance=request.user)
        return render(request, 'accounts/account_personal_information_edit.html', {'form': user_edit_form})


class AccountPersonalOrders(View):
    """ Show customer orders """

    def get(self, request):
        customer = AccountSystem.get_customer_account(request)
        carts = CartSystem.get_customer_in_order_carts(customer=customer)
        orders = OrderSystem.get_user_orders(customer=customer, cart=carts)
        order_items = OrderSystem.get_order_items()
        return render(request, 'accounts/account_orders.html', {'orders': orders, 'order_items': order_items})


class AccountRegistrationView(View):
    """ Registration customer account """

    def post(self, request):
        form = RegistrationForm(request.POST)
        form = AccountSystem.registration(
            self=AccountSystem, request=request, form=form)
        if form.errors:
            return render(request, 'accounts/registration/registration.html', {'form': form})
        else:
            return render(request, 'accounts/registration/registration_valid.html')


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:account')
        form = RegistrationForm()
        return render(request, 'accounts/registration/registration.html', {'form': form})


def account_activate(request, uidb64, token):
    """ Activation customer account using token """

    try:
        user = AccountSystem.get_user_uid(uidb64=uidb64)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        AccountSystem.activation_customer_account(request, user=user)
        return redirect('accounts:account')
    else:
        messages.add_message(request, messages.SUCCESS,
                             "Невдала спроба активації вашого акаунту, повторіть спробу")
        return redirect('accounts:account_registration')
