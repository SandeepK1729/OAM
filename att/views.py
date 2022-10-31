from django.shortcuts import render, HttpResponse
from .models import Department

def departments(request):
    return render(request, 'views.html', {
        'departments' : Department.objects.all()
    })