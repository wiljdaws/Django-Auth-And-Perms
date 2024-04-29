from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Professor, Office, Section


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        base_email = f"{user.first_name[0]}{user.last_name}@dallascollege.edu"
        email = base_email
        increment = 1

        while User.objects.filter(email=email).exists():
            email = f"{base_email}{increment}"
            # get everything before the @
            increment += 1

        user.email = email
        user.username = email.split('@')[0]

        if commit:
            user.save()
        return user


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'professor', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')

        if start_date:
            if start_date.month >= Course.SPRING_START_MONTH and start_date.month < Course.SUMMER_START_MONTH:
                semester = 'Spring'
            elif start_date.month >= Course.SUMMER_START_MONTH and start_date.month < Course.FALL_START_MONTH:
                semester = 'Summer'
            elif start_date.month >= Course.FALL_START_MONTH and start_date.month < Course.WINTER_START_MONTH:
                semester = 'Fall'
            else:
                semester = 'Winter'

            cleaned_data['semester'] = semester

        return cleaned_data

from datetime import timedelta

class SectionForm(forms.ModelForm):
    WEEK_CHOICES = [
        (4, '4 weeks'),
        (6, '6 weeks'),
        (12, '12 weeks'),
        (18, '18 weeks'),
    ]

    weeks = forms.ChoiceField(choices=WEEK_CHOICES)
    #end_date = forms.DateTimeField(widget=forms.HiddenInput()) 
    
    class Meta:
        model = Section
        fields = ['id', 'section_number', 'name', 'description', 'professor', 'start_date', 'weeks']
        # Removed 'end_date' from fields

    def clean(self):
        print("Clean method is called")  # Add this line
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        weeks = cleaned_data.get('weeks')

        if start_date:
            if start_date.month >= Section.SPRING_START_MONTH and start_date.month < Section.SUMMER_START_MONTH:
                semester = 'Spring'
            elif start_date.month >= Section.SUMMER_START_MONTH and start_date.month < Section.FALL_START_MONTH:
                semester = 'Summer'
            elif start_date.month >= Section.FALL_START_MONTH and start_date.month < Section.WINTER_START_MONTH:
                semester = 'Fall'
            else:
                semester = 'Winter'

            cleaned_data['semester'] = semester

        if start_date and weeks:
            # Calculate the end date by adding the number of weeks to the start date
            end_date = start_date + timedelta(weeks=int(weeks))

            # Update the cleaned_data dictionary with the calculated end date
            cleaned_data['end_date'] = end_date
            #print(f"{end_date = }")

        return cleaned_data

class ProfessorForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Professor
        fields = ['first_name', 'last_name', 'phone_number', 'office_location']

    def save(self, commit=True):
        professor = super().save(commit=False)
        professor.name = f"{professor.first_name} {professor.last_name}"
        base_email = f"{professor.first_name[0]}{professor.last_name}@dallascollege.edu"
        email = base_email
        increment = 1

        while Professor.objects.filter(email=email).exists():
            email = f"{base_email}{increment}"
            increment += 1

        professor.email = email

        if commit:
            professor.save()
        return professor

class OfficeForm(forms.ModelForm):
    building = forms.CharField(required=True)
    room_number = forms.IntegerField(required=True)
    address = forms.CharField(required=True)
    
    class Meta:
        model = Office
        fields = ['building', 'room_number', 'address']  
    
    