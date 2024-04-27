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

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['id', 'section_number', 'name', 'description', 'professor', 'start_date', 'end_date']

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
    
    