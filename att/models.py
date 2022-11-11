from django.db import models
from core.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

time_slots = (
    ("1st period",  '9:10 - 10:10'),
    ("2nd period", '10:10 - 11:10'),
    ('3rd period', '11:10 - 12:10'),
    ('4th period', '01:00 - 02:00'),
    ('5th period', '02:00 - 03:00'),
    ('6th period', '03:00 - 04:00'),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

class Department(models.Model):
    name = models.CharField(_("Name of the Department"), max_length=200)#, choices = dept_types, default=dept_types[7][1])
    short_name = models.CharField(max_length = 10, primary_key = True)

    def __str__(self):
        return self.short_name

class Subject(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50, default='X')
    # link = models.URLField()

    def __str__(self):
        return self.name

class Batch(models.Model):
    year_choices = (
        ("1st Year", "I"),
        ("2nd Year", "II"),
        ("3rd Year", "III"),
        ("4th Year", "IV")
    )
    start_year = models.IntegerField()
    year       = models.CharField(choices = year_choices, max_length = 10)
    class Meta:
        verbose_name_plural = 'Batches'
        

    def __str__(self):
        return f"{self.year}"

class Student(models.Model):
    user    = models.OneToOneField(
                User, 
                on_delete=models.CASCADE,
                primary_key = True,
                # parent_link = True,
                # related_name = 'student'
            )
    roll_no = models.CharField(_("Roll no"), max_length = 10, editable = True)
    
    primary_mobile  = models.CharField(
                _("Student Mobile no."), 
                max_length = 13,
                null = True,
                blank = True
            )
    secondary_mobile  = models.CharField(
                _("Student Secondary Mobile no."), 
                max_length = 13,
                null = True,
                blank = True,
            )
    
    father_name = models.CharField(
                _("Father Name"), 
                max_length = 50,
                null = True,
                blank = True
            )
    mother_name = models.CharField(
                _("Mother Name"), 
                max_length = 50,
                null = True,
                blank = True
            )
    
    father_mobile = models.CharField(
                _("Father Mobile"), 
                max_length = 50,
                null = True,
                blank = True,
            )
    mother_mobile = models.CharField(
                _("Mother Mobile"), 
                max_length = 50,
                null = True,
                blank = True
            )
    
    branch  = models.ForeignKey(
                Department,
                on_delete = models.CASCADE,
                verbose_name = "belongs to department",
            )
    year    = models.ForeignKey(Batch, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'students'
    
    def __str__(self):
        return f"{self.roll_no} - {self.user.first_name} {self.user.last_name}"

class Staff(models.Model):
    user    = models.OneToOneField(
                User, 
                on_delete=models.CASCADE, 
                primary_key = True,
                #parent_link = True,
                #related_name = 'staff'
            )
    qualification   = models.CharField(null = True, blank = True, max_length = 20)
    designation     = models.CharField(null = True, blank = True, max_length = 20)
    specialization  = models.CharField(null = True, blank = True, max_length = 20)
    experience      = models.IntegerField(null = True, blank = True)
    jntu_id         = models.CharField(null = True, blank = True, max_length = 20)
    
    def __str__(self):
        return f"{self.user}"

class Period(models.Model):
    date        = models.DateField(default = timezone.now)
    hour        = models.CharField(max_length = 15, choices = time_slots)
    
    def __str__(self):
        return f" {self.hour} on {self.date}"

class Section(models.Model):
    name        = models.CharField(max_length = 10, primary_key = True)
    dept        = models.ForeignKey(Department, on_delete=models.CASCADE)
    subjects    = models.ManyToManyField(Subject)# on_delete=models.CASCADE)
    students    = models.ManyToManyField(Student)
    staffs      = models.ManyToManyField(Staff)
    periods     = models.ManyToManyField(Period)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    section     = models.ForeignKey(Section, on_delete = models.CASCADE)
    period      = models.ForeignKey(Period,  on_delete = models.CASCADE)
    subject     = models.ForeignKey(Subject, on_delete = models.CASCADE)
    student     = models.ForeignKey(Student, on_delete = models.CASCADE)
    student_status = models.CharField(
                    max_length = 10, 
                    choices = (
                        ('Absent', 'A'), 
                        ('Present', 'P')
                    )
                )

    def __str__(self) -> str:
        return f"{self.student.user.first_name} {self.student.user.last_name} is {self.student_status} for {self.period}"