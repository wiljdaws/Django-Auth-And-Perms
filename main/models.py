from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='Default Course Name')
    description = models.CharField(max_length=200, default='Default Description')
    professor = models.ForeignKey(Professor, related_name='courses', on_delete=models.CASCADE)
    semester = models.CharField(max_length=50, default='Default Semester')
    
    def __str__(self):
        return self.name

