from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    
    path('', admin.site.urls),
    path('api/', include('api.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/', include('ai.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),
    # path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
#     path('admin/', admin.site.urls),
# )