from django.urls import path, include

# core views
from . import views

urlpatterns = [
    path('departments', views.departments, name = 'departments'),
    
]