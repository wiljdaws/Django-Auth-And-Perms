from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Professor


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
        fields = ['name', 'description', 'professor', 'semester']
    
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['professor'].queryset = Professor.objects.all()


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