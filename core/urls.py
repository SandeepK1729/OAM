from django.urls import path, include

# core views
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about', views.about, name = 'about'),
    path('accounts/signup', views.signup, name = 'signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]