from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings 
from django.conf.urls.static import static
from django.views.static import serve

# core app urls 
from core import urls as coreUrls

urlpatterns = [
    path('', include(coreUrls)),
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>)', serve, {'document_root' : settings.MEDIA_ROOT})
]

# is settings.DEBUG:
urlpatterns += static(
    settings.STATIC_URL,
    document_root = settings.STAICFILES_ROOT[0]
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
)
