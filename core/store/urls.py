from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.BaseView.as_view(), name='home_page'),

    path('search/', views.search_product, name='search'),

    path('products/', views.ProductListView.as_view(), name='products_list'),

    path('products/price/<str:min_price>/<str:max_price>/',
         views.ProductListView.as_view(), name='product_list_by_price'),


    path('products/category/<slug:category_slug>/',
         views.ProductListView.as_view(), name='product_list_by_category'),

    path('products/brand/<slug:brand_slug>/', views.ProductListView.as_view(),
         name='product_list_by_brand'),



    path('product/<slug:ct_model>/<slug:product_slug>/',
         views.ProductDetailView.as_view(), name='product_detail'),
]
