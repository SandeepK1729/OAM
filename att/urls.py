from django.urls import path, include

# core views
from . import views

urlpatterns = [
    path('departments', views.departments, name = 'departments'),
    path('department/<str:dept>', views.view_sections, name = 'department sections'),

    path(
        'mark_attendance', 
        views.view_sections, 
        name = 'view_sections'
    ),
    
    path(
        'show_attendance/<str:section_name>', 
        views.show_attendance, 
        name='show attendance'
    ),
    
    path(
        'mark_attendance/<str:section_name>/new', 
        views.mark_attendance, 
        name='mark attendance'
    ),
    
    path(
        'update_attendance/<str:section_name>/<int:period_id>', 
        views.update_marked_attendance, 
        name='update attendance'
    ),
]