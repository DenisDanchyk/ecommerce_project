from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='card')),
    path('order/', include('orders.urls', namespace='orders')),
    path('wish/', include('wish.urls', namespace='wish')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('', include('store.urls', namespace='store')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
