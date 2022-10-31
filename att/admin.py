from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Section)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Batch)
admin.site.register(Period)
admin.site.register(Attendance)

from .helper import help
#help()