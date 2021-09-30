from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),

]
