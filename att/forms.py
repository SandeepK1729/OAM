from django import forms  
from django.utils import timezone
from .models import time_slots, Student
import datetime 

class AttendanceMarkForm(forms.Form):
    date    = forms.DateField(initial=datetime.date.today)
    hour    = forms.ChoiceField(choices = time_slots)#, max_length= 10)
    """presentees = forms.ArrayField(
                forms.ChoiceField(choices = time_slots),
            )"""
    
    presentees = forms.MultipleChoiceField(
                    choices = time_slots
                )

    # li = SimpleArrayField(forms.CharField(max_length=100))
