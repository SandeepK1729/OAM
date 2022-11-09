from django.urls import path, include

# core views
from . import views

urlpatterns = [
    path('departments', views.departments, name = 'departments'),

    path(
        'mark_attendance', 
        views.view_sections, 
        name = 'view_sections'
    ),
    path(
        'mark_attendance/<str:section_name>/new', 
        views.mark_attendance, 
        name='mark attendance'
    ),
    path(
        'mark_attendance/<str:section_name>/<int:period_id>', 
        views.update_marked_attendance, 
        name='update marked attendance'
    ),
]