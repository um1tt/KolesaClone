from django.contrib import admin
from django.urls import path, include
from listings.views import home  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('accounts.urls')),
    path('api/', include('listings.urls')),
    path('api/listings/', include('listings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
