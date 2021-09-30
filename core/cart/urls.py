from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<slug:ct_model>/<slug:product_slug>',
         views.AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<slug:ct_model>/<slug:product_slug>/',
         views.DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-product-quantity/<slug:ct_model>/<slug:product_slug>/',
         views.ChangeQuantityView.as_view(), name='change_product_quantity'),
]
