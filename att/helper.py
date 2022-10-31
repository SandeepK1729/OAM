from .models import *

def dept():
    dept_types = (
                    ('CSE', 'Computer Science & Engineering'),
                    ('ECE', 'Electronics & Communication Engineering'),
                    ('EEE', 'Electronics & Electrical Engineering'),
                    ('MECH', 'Mechanical Engineering'),
                    ('CIV', 'Civil Engineering'),
                    ('IT', 'Information Technology'),
                    ('CSC', 'Computer Science & Engineering - Cybersecurity'),
                    ('CSM', 'Computer Science & Engineering - Artificial Intelligence & Machine Learning'),
                    ('AIDS', 'Artificial Intelligence & Machine Learning and Data Science'),   
                )

    for short_name, name in dept_types:
        dept = Department.objects.create(short_name = short_name, name = name)

    print("Done with department ... OK")

def help():
    dept()
