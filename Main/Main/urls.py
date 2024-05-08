from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name='Home'),
    path('accounts/', include('accounts.urls'), name='Accounts'),
    path('products/', include('products.urls'), name='Products'),
    path('Cart/',include('cart.urls'),name='cart'),
    path('Order/', include('order.urls'), name='order')

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)