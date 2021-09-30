from django.urls import path

from . import views

app_name = 'coupons'

urlpatterns = [
    path('apply/', views.ApplyCouponView.as_view(), name='apply_coupon'),
]
