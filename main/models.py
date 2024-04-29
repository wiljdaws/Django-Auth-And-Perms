import re
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from numpy import add

class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100, blank=True)  
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20)
    office_location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def validate_year(value):
    current_year = timezone.now().year
    if value.year < current_year or value.year > current_year + 5:
        raise ValidationError(f"Year must be between {current_year} and {current_year + 5}")

class Course(models.Model):
    SPRING_START_MONTH = 3
    SUMMER_START_MONTH = 6
    FALL_START_MONTH = 9
    WINTER_START_MONTH = 12

    id = models.AutoField(primary_key=True)
    course_number = models.CharField(max_length=10)
    name = models.CharField(max_length=50, default='Default Course Name')
    description = models.CharField(max_length=200, default='Default Description')
    professor = models.ForeignKey(Professor, related_name='courses', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now, validators=[validate_year])
    end_date = models.DateField(default=timezone.now, validators=[validate_year])

    def semester(self):
        if self.start_date.month >= self.SPRING_START_MONTH and self.start_date.month < self.SUMMER_START_MONTH:
            return 'Spring'
        elif self.start_date.month >= self.SUMMER_START_MONTH and self.start_date.month < self.FALL_START_MONTH:
            return 'Summer'
        elif self.start_date.month >= self.FALL_START_MONTH and self.start_date.month < self.WINTER_START_MONTH:
            return 'Fall'
        else:
            return 'Winter'

    def __str__(self):
        return f"{self.name} - {self.semester()} {self.start_date.year}"

class Section(models.Model):
    SPRING_START_MONTH = 3
    SUMMER_START_MONTH = 6
    FALL_START_MONTH = 9
    WINTER_START_MONTH = 12

    id = models.AutoField(primary_key=True)
    section_number = models.CharField(max_length=5)
    name = models.CharField(max_length=50, default='Default Section Name')
    description = models.CharField(max_length=200, default='Default Description')
    professor = models.ForeignKey(Professor, related_name='sections', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now, validators=[validate_year])
    end_date = models.DateField(default=timezone.now, validators=[validate_year])
    course_code = models.CharField(max_length=4, default='Course Code')
    subject = models.CharField(max_length=50, default='Default Subject')
    meeting_info = models.CharField(max_length=50, default='Meeting Information')
    seat_capacity = models.IntegerField()
    credit = models.IntegerField()
    grading = models.CharField(max_length=50, default='Grading Method')
    requisites = models.CharField(max_length=200, default='Requisites Needed')
    topic = models.CharField(max_length=200, default='Topic')

    def semester(self):
        if self.start_date.month >= self.SPRING_START_MONTH and self.start_date.month < self.SUMMER_START_MONTH:
            return 'Spring'
        elif self.start_date.month >= self.SUMMER_START_MONTH and self.start_date.month < self.FALL_START_MONTH:
            return 'Summer'
        elif self.start_date.month >= self.FALL_START_MONTH and self.start_date.month < self.WINTER_START_MONTH:
            return 'Fall'
        else:
            return 'Winter'

    def __str__(self):
        return f"{self.name} - {self.semester()} {self.start_date.year}"
    
class Office(models.Model):
    building = models.CharField(max_length=100)
    room_number = models.IntegerField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.building}, {self.address}"

