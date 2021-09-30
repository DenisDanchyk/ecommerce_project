from django.urls import path

from . import views

app_name = 'wish'

urlpatterns = [
    path('', views.WishView.as_view(), name='wish'),
    path('add-to-wish/<slug:ct_model>/<slug:product_slug>',
         views.AddToWishView.as_view(), name='add_to_wish'),
    path('delete-from-wish/<slug:ct_model>/<slug:product_slug>/',
         views.DeleteWishView.as_view(), name='delete_from_wish')
]
