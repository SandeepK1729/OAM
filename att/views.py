from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .decorators import faculty_login_required
from django.utils.translation import gettext_lazy as _

from .models    import Department, Section, Period, time_slots, Attendance, Subject, Student
from .forms     import AttendanceMarkForm
from core.models import User

from .acadamic_data import acadamics
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
        return redirect(f'/show_attendance/{section}/')
        
    
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
        return redirect(f'/show_attendance/{section}/')
        
    return render(request, 'mark_attendance.html', context)

@login_required
@faculty_login_required
def show_attendance(request, section_name):
    section     = Section.objects.get(name = section_name)
    periods     = section.periods.all()
    section_attendance = Attendance.objects.filter(section=section)

    ids, hours, dates, subjects, presentees, absentees = [], [], [], [], [], []

    for each_period in periods:
        student_attendance = section_attendance.filter(period = each_period).all()
        
        try:
            subjects.append(student_attendance.first().subject.short_name)
        except:
            continue
        
        print(student_attendance)
        
        ids.append(each_period.id)
        dates.append(each_period.date)
        hours.append(each_period.hour)
        # print(student_attendance)
        
        # print(student_attendance)

        p, a = 0, 0 
        for each_student in student_attendance:
            if each_student.student_status == 'Present':
                p += 1
            else:
                a += 1 
        presentees.append(p)
        absentees.append(a)
    print(ids, dates, hours, subjects, absentees)
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
    
    return render(request, 'student_details.html', {
        'atts' : atts,
        'section' : atts.first().section,
    })

def get_classes_count(section, subject, student):
    return Attendance.objects.filter(
                    section = section, 
                    subject = subject,
                    student = student,
                ).count()

def get_present_classes_count(section, subject, student):
    return Attendance.objects.filter(
                    section = section, 
                    subject = subject,
                    student = student,
                    student_status = "Present",
                ).count()

@login_required
@faculty_login_required
def show_report(request, section_name):
    section     = Section.objects.get(name = section_name)
    students    = section.students.all()
    subjects    = section.subjects.all()

    total_classes = {
        subject.name : get_classes_count(section, subject, students.first()) for subject in subjects
    }

    header = ["Roll no"] + [
                f"{subject.short_name} ({get_classes_count(section, subject, students.first())})" for subject in subjects
                    ] + ["Percentage"]

    data = []

    for student in students:
        row = [student.roll_no]
        per = 0 
        for subject in subjects:
            present_count = get_present_classes_count(section, subject, student)
            row.append(present_count)
            per += 1 if total_classes[subject.name] == 0 else present_count / total_classes[subject.name]
        row.append(round(per * 100 / len(total_classes), 2))
        data.append(row)
        
    return render(request, 'table.html', {
        'headers' : header,
        'data' : data,
    })

@login_required
def acadamic_info(request):
    header = ["Name", "Notes Link"]
    data   = [[name, link] for name, link in acadamics.items()]
    
    return render(request, 'links.html', {
        'headers' : header,
        'data' : data,
    })

@login_required
def show_student_report(request, section_name):
    section     = Section.objects.get(name = section_name)
    student     = Student.objects.get(user = request.user)
    subjects    = section.subjects.all()

    total_classes = {
        subject.name : get_classes_count(section, subject, student) for subject in subjects
    }

    per = 0 
    
    counts = ["Present Count"]
    percen = ["Percentage"] 

    for subject in subjects:
        present_count = get_present_classes_count(section, subject, student)
        counts.append(present_count)

        percentage_of_subject = round((1 if total_classes[subject.name] == 0 else present_count / total_classes[subject.name]) * 100, 2)
        percen.append(percentage_of_subject)
        
        per += percentage_of_subject
    
    return render(request, 'table.html', {
        'headers'   : ["Roll no"] + [
                f"{subject.short_name} ({get_classes_count(section, subject, student)})" for subject in subjects
                    ],
        'data'      : [counts, percen],
        'percentage': per / subjects.count(),
        'include_percentage' : True,
    })