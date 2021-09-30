from django.urls import path
from django.contrib.auth import views as auth_view

from . import views
from .forms import UserLoginForm

app_name = 'accounts'

urlpatterns = [
    path('', views.account, name='account'),
    path('personal_information/', views.account_personal_information, name='personal_information'),
    path('personal_orders/', views.AccountPersonalOrders.as_view(), name='personal_orders'),
    path('edit_information/', views.EditPersonalInformation.as_view(), name='edit_information'),


    path('registration/', views.AccountRegistrationView.as_view(),
         name='account_registration'),
    path('activate/<slug:uidb64>/<slug:token>)/',
         views.account_activate, name='activate_account'),
    path('login/', auth_view.LoginView.as_view(template_name='accounts/registration/login.html',
         form_class=UserLoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='/account/login/'), name='logout'),
]
