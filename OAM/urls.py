from django.contrib import admin
from django.urls import path, include

# core app urls 
from core import urls as coreUrls

urlpatterns = [
    path('', include(coreUrls)),
    path('admin/', admin.site.urls),
]
