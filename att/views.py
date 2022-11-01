from django.shortcuts import render, HttpResponse
from .models import Department, Section
from django.contrib.auth.decorators import login_required
from .decorators import faculty_login_required

@login_required
@faculty_login_required
def departments(request):
    return render(request, 'views.html', {
        'departments' : Department.objects.all()
    })

@login_required
@faculty_login_required
def mark_attendance(request, section_name):
    sections = Section.objects.get(name = section_name)
    if request.method == 'POST':
        pass    
    
    #print(sections.subjects.objects.add(name = "Python", short_name="APP"))
    return render(request, 'mark_attendance.html', {
        'section' : sections,
    })