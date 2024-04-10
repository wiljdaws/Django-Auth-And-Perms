from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Professor
from django.forms import ModelForm
from datetime import datetime
from django.contrib.auth import login, logout
from .forms import RegisterForm, CourseForm, ProfessorForm

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'professor', 'semester']

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

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

def courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/courses')
    else:
        form = CourseForm()
        courses = Course.objects.all()
        professors = Professor.objects.all()
        current_year = datetime.now().year
        return render(request, 'main/courses.html', {'form': form, 'courses': courses, 'professors': professors, 'current_year': current_year})


@staff_member_required
def add_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/professors')
    else:
        form = ProfessorForm()
    return render(request, 'main/add_professor.html', {'form': form})

@staff_member_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'main/add_course.html', {'course_form': form})

@staff_member_required
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    professors = Professor.objects.all()  # Fetch all professors
    current_year = datetime.now().year
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('/courses')
    else:
        form = CourseForm(instance=course)
        return render(request, 'main/edit_course.html', {'form': form, 'course': course, 'professors': professors, 'current_year': current_year})

@staff_member_required
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.delete()
        return redirect('/courses')
    return render(request, 'main/delete_course.html', {'course': course})

def professors(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/professors')
    else:
        form = ProfessorForm()
        professors = Professor.objects.all()
        return render(request, 'main/professors.html', {'form': form, 'professors': professors})



def logout_view(request):
    logout(request)
    return redirect('home')

@staff_member_required
def edit_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('/professors')
    else:
        form = ProfessorForm(instance=professor)
        return render(request, 'main/edit_professor.html', {'form': form, 'professor': professor})

@staff_member_required
def delete_professor(request, id):
    professor = get_object_or_404(Professor, id=id)
    if request.method == 'POST':
        professor.delete()
        return redirect('/professors')

def home(request):
    return render(request, 'main/index.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            original_username = form.cleaned_data.get('username')
            if not original_username:
                form.add_error('username', 'This field is required.')
                return render(request, 'registration/sign_up.html', {'form': form})
            username = original_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = original_username + str(counter)
                counter += 1
            user = User.objects.create_user(username=username, password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})