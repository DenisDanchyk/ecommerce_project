from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'orders'


urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    path('invalid_order/', TemplateView.as_view(template_name='orders/order_invalid.html'), name='invalid_order'),

]
