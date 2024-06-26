from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from core.views import index

urlpatterns = [
    # path('admin/', admin.site.urls),

    # path('', include('core.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('products/', include(('products.urls', 'products'), namespace='products')),
    # path('cart/', include('cart.urls')),

    path('admin/', admin.site.urls),
    path('', include('core.urls')),  
    path('cart/', include('cart.urls')),  
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
