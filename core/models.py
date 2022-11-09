from datetime import date
from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)
user_types = (
    ('student', 'student'),
    ('faculty', 'faculty'),
    ('admin'  , 'admin')  ,
)

class User(AbstractUser):
    # CustomUser model will be act as General class of parent
    user_type        = models.CharField(
                    max_length = 10, 
                    choices = user_types,
                    default='student',
                    null = False,
                )
    gender      = models.CharField(
                    max_length=50, 
                    choices=sex_choice, 
                    default='Male'
                )
    dob         = models.DateField(
                    _("date of birth"),
                    default=date.today,
                    null = True,
                    blank = True,
                    help_text="Please use the following format: <em>YYYY-MM-DD</em>."
                )
    
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    
    class Meta:
        ordering    = [
                        'first_name', 
                        'last_name', 
                        'dob', 
                        'email', 
                        'gender'
                    ]   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"