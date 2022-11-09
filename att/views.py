from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import faculty_login_required
from django.utils.translation import gettext_lazy as _

from .models    import Department, Section, Period, time_slots, Attendance, Subject
from .forms     import AttendanceMarkForm

import datetime 

@login_required
@faculty_login_required
def departments(request):
    return render(request, 'views.html', {
        'departments' : Department.objects.filter()
    })

@login_required
@faculty_login_required
def view_sections(request):
    if request.method == 'POST':
        pass    
    return render(request, 'choose_list.html', {
        'sections' : Section.objects.all(),
    })

@login_required
@faculty_login_required
def mark_attendance(request, section_name):
    section  = Section.objects.get(name = section_name)
    subjects = section.subjects.all()
    students = section.students.all()

    context = {
        'today'     : datetime.date.today().strftime("%Y-%m-%d"),
        'periods'   : time_slots,
        'sections'  : section,
        'subjects'  : subjects,
        'students'  : students,
    }

    if request.method == 'POST':
        date    = request.POST['date'] 
        hour    = request.POST['hour']
        subject = request.POST['subject']
        status  = request.POST['status']
        members = request.POST

        period = Period(date = date, hour = hour)
        period.save()
        
        for student in students:
            att = Attendance(
                period = period,
                student = student,
                subject = Subject.objects.filter(name = subject).first(),
                student_status = "Present" if student.roll_no in members and status == "p" else "Absent"
            )
            print(att)
            att.save()
        
        context.update(request.POST)
        print(date, hour, subject, status, members)
    
    return render(request, 'mark_attendance.html', context)

@login_required
@faculty_login_required
def update_marked_attendance(request, section_name, period_id = 0):
    section  = Section.objects.get(name = section_name)
    subjects = section.subjects.all()
    students = section.students.all()

    if request.method == 'POST':
        date    = request.POST['date'] 
        hour    = request.POST['hour']
        subject = request.POST['subject']
        status  = request.POST['status']
        members = request.POST

        period = Period(date = date, hour = hour)
        period.save()

        for student in students:
            att = Attendance(
                period = period,
                student = student,
                student_status = "Present" if student.roll_no in members and status == "P" else "Absent"
            )
            att.save()
        print(date, hour, subject, status, members)
    
    return render(request, 'mark_attendance.html', {
        'today' :  datetime.date.today().strftime("%Y-%m-%d"),
        'periods'  : time_slots,
        'sections' : section,
        'subjects' : subjects,
        'students' : students,
        # 'form' : form,
    })
