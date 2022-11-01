from django.urls import path, include

# core views
from . import views

urlpatterns = [
    path('departments', views.departments, name = 'departments'),
    #path('sections', views.sections, name = 'sections'),
    path('mark_attendance/<str:section_name>', views.mark_attendance, name='mark attendance'),
]