import uuid
from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100, blank=True)  
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20)
    office_location = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name, self.last_name, self.email, self.phone_number, self.office_location


from django.db import models

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.PositiveIntegerField(default=0, unique=True)
    name = models.CharField(max_length=50, default='Default Course Name')
    description = models.CharField(max_length=200, default='Default Description')
    professor = models.ForeignKey(Professor, related_name='courses', on_delete=models.CASCADE)
    semester = models.CharField(max_length=50, default='Default Semester')
    
    def __str__(self):
        return self.name

