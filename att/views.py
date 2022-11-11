from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .decorators import faculty_login_required
from django.utils.translation import gettext_lazy as _

from .models    import Department, Section, Period, time_slots, Attendance, Subject, Student
from .forms     import AttendanceMarkForm
from core.models import User

import datetime 

@login_required
@faculty_login_required
def departments(request):
    # print(request.user.staff_set)
    return render(request, 'depts.html', {
        'departments' : Department.objects.filter()
    })

@login_required
@faculty_login_required
def view_sections(request, dept = ""):
    department = Department.objects.get(short_name = dept)

    if request.method == 'POST':
        pass    
    return render(request, 'choose_list.html', {
        'sections' : Section.objects.filter(dept = department),
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
        
        section.periods.add(period)
        print(period.id)

        for student in students:
            attendance_status = "Present" if (status == "p" and student.roll_no in members) or (status == "a" and student.roll_no not in members) else "Absent"
            
            att = Attendance(
                section = section,
                period = period,
                student = student,
                subject = Subject.objects.filter(name = subject).first(),
                student_status = attendance_status
            )
            att.save()
        return redirect(f'/show_attendance/{section}')
        
        # context.update(request.POST)
    
    return render(request, 'mark_attendance.html', context)

@login_required
@faculty_login_required
def update_marked_attendance(request, section_name, period_id = 0):
    section  = Section.objects.get(name = section_name)
    subjects = section.subjects.all()
    students = section.students.all()

    context = {
        'today'     : datetime.date.today().strftime("%Y-%m-%d"),
        'periods'   : time_slots,
        'subjects'  : subjects,
        'students'  : students,
    }

    period      = Period.objects.get(pk = period_id)
    attendances = Attendance.objects.filter(section = section, period = period)
    
    additional_context = {
        'today'     : period.date.strftime("%Y-%m-%d"),
        'hour'      : period.hour,
        'subject'   : attendances.first().subject,
        'presentees': [p.student for p in attendances.filter(student_status = 'Present')],
        'absentees' : [a.student for a in attendances.filter(student_status = 'Absent' )],
    }

    context.update(additional_context)

    if request.method == 'POST':
        date    = request.POST['date'] 
        hour    = request.POST['hour']
        subject = Subject.objects.get(
                    name = request.POST['subject']
                )
        status  = request.POST['status']
        members = request.POST

        
        period.delete()
        period = Period(date = date, hour = hour)
        period.save()
        section.periods.add(period)
        print(period.id)

        for student in students:
            att = Attendance(
                section = section,
                period = period,
                student = student,
                subject = Subject.objects.get(name = subject),
                student_status = "Present" if student.roll_no in members and status == "p" else "Absent"
            )
            att.save()
        return redirect(f'/show_attendance/{section}')
        
    return render(request, 'mark_attendance.html', context)

@login_required
@faculty_login_required
def show_attendance(request, section_name):
    section     = Section.objects.get(name = section_name)
    periods     = Section.objects.get(name = section_name).periods.all()
    section_attendance = Attendance.objects.filter(section=section)

    ids, hours, dates, subjects, presentees, absentees = [], [], [], [], [], []
    
    for each_period in periods.all():
        student_attendance = section_attendance.filter(period = each_period).all()

        ids.append(each_period.id)
        dates.append(each_period.date)
        hours.append(each_period.hour)
        subjects.append(student_attendance[0].subject)
        
        print(student_attendance)

        p, a = 0, 0 
        for each_student in student_attendance:
            if each_student.student_status == 'Present':
                p += 1
            else:
                a += 1 
        presentees.append(p)
        absentees.append(a)

    return render(request, 'show_periods.html', {
        'periods' : zip(
                        ids, 
                        dates,
                        hours,
                        subjects, 
                        presentees, 
                        absentees
                    ),
         'section' : section,
    })

@login_required
def student_home(request):
    user        = User.objects.get(username = request.user.username)
    student     = Student.objects.get(user = user)

    atts = Attendance.objects.filter(student = student)

    print(atts)
    return render(request, 'student_details.html', {
        'atts' : atts,
    })