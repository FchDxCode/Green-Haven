from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('admin/'), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/', include('ai.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)