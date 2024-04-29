from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Professor, Office, Section
from django.forms import ModelForm
from datetime import datetime
from django.contrib.auth import login, logout
from .forms import RegisterForm, CourseForm, ProfessorForm, OfficeForm, SectionForm

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['id', 'course_number', 'name', 'description', 'professor', 'start_date', 'end_date']

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

    class Meta:
        model = Section
<<<<<<< HEAD
        fields = ['id', 'section_number', 'name', 'professor', 'description', 'start_date', 'end_date', 'course_code', 'subject', 'meeting_info', 'seat_capacity', 'credit', 'grading', 'requisites', 'topic']
=======
        fields = ['id', 'section_number', 'name', 'description', 'professor', 'start_date', 'weeks']
>>>>>>> f637bc07289fd58268ecde50beba654626e649cd

    def clean(self):
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

        return cleaned_data

class ProfessorForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    office_location = forms.ModelChoiceField(queryset=Office.objects.all())

    class Meta:
        model = Professor
        fields = ['first_name', 'last_name', 'phone_number', 'office_location']

    def save(self, commit=True):
        professor = super().save(commit=False)
        professor.first_name = professor.first_name.capitalize()
        professor.last_name = professor.last_name.capitalize()
        professor.name = f"{professor.first_name} {professor.last_name}"
        base_email = f"{professor.first_name[0]}{professor.last_name}".lower()  # Convert to lowercase
        domain = "@dallascollege.edu"
        email = base_email + domain
        increment = 1
    
        while Professor.objects.filter(email__iexact=email).exists():
            email = f"{base_email}{increment}{domain}"
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
        form.clean()
        if form.is_valid():
            form.save()
            return redirect('/courses')
    else:
        courses = Course.objects.all()

        course_number = request.GET.get('course_number')
        if course_number:
            courses = courses.filter(course_number__icontains=course_number)

        course_name = request.GET.get('course_name')
        if course_name:
            courses = courses.filter(name__icontains=course_name)
        form = CourseForm()
        professors = Professor.objects.all()
        current_year = datetime.now().year
        return render(request, 'main/courses.html', {'form': form, 'courses': courses, 'professors': professors, 'current_year': current_year})

def sections(request):
    if request.method == 'POST':
        section_form = SectionForm(request.POST)
        section_form.clean()
        if section_form.is_valid():
            print(f"End date: {section_form.cleaned_data['end_date']}")
            section_form.save()
            return redirect('/sections')
    else:
        sections = Section.objects.all()

        section_number = request.GET.get('section_number')
        if section_number:
            sections = sections.filter(section_number__icontains=section_number)

        section_name = request.GET.get('section_name')
        if section_name:
            sections = sections.filter(name__icontains=section_name)
<<<<<<< HEAD
        
        form = SectionForm()

=======
        section_form = SectionForm()
>>>>>>> f637bc07289fd58268ecde50beba654626e649cd
        professors = Professor.objects.all()

        current_year = datetime.now().year
<<<<<<< HEAD

        course_code = request.GET.get('course_code')
        if course_code:
            sections = sections.filter(course_code__icontains=course_code)

        subject = request.GET.get('subject')
        if subject:
            sections = sections.filter(subject__icontains=subject)

        meeting_info = request.GET.get('meeting_info')
        if meeting_info:
            sections = sections.filter(meeting_info__icontains=meeting_info)

        seat_capacity = request.GET.get('seat_capacity')
        if seat_capacity:
            sections = sections.filter(seat_capacity__icontains=seat_capacity)

        credit = request.GET.get('credit')
        if credit:
            sections = sections.filter(credit__icontains=credit)

        grading = request.GET.get('grading')
        if grading:
            sections = sections.filter(grading__icontains=grading)

        requisites = request.GET.get('requisites')
        if requisites:
            sections = sections.filter(requisites__icontains=requisites)
            
        topic = request.GET.get('topic')
        if topic:
            sections = sections.filter(topic__icontains=topic)
       
        return render(request, 'main/sections.html', {'form': form, 'sections': sections, 'professors': professors, 'current_year': current_year, 'course_code': course_code, 'subject': subject, 'meeting_info': meeting_info, 'seat_capacity': seat_capacity, 'credit': credit, 'grading': grading, 'requisites': requisites, 'topic': topic})
=======
        return render(request, 'main/sections.html', {'section_form': section_form, 'sections': sections, 'professors': professors, 'current_year': current_year})
>>>>>>> f637bc07289fd58268ecde50beba654626e649cd

class OfficeForm(forms.ModelForm):
    building = forms.CharField(required=True)
    room_number = forms.IntegerField(required=True)
    address = forms.CharField(required=True)
    
    class Meta:
        model = Office
        fields = ['building', 'room_number', 'address']  

def office(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/offices')
    else:
        form = OfficeForm()
        offices = Office.objects.all()
        return render(request, 'main/offices.html', {'office_form': form, 'offices': offices})

<<<<<<< HEAD
=======
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
    
    def save(self, commit=True):
        # Call the original save method to save the fields included in the form
        section = super().save(commit=False)

        # Update the end_date field manually
        section.end_date = self.cleaned_data['end_date']

        if commit:
            section.save()
        return section

>>>>>>> f637bc07289fd58268ecde50beba654626e649cd
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
def add_office(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offices')
    else:
        form = OfficeForm()
    return render(request, 'main/add_office.html', {'office_form': form})

@staff_member_required
def offices(request):
    offices = Office.objects.all()
    return render(request, 'main/offices.html', {'office_form': offices})

@staff_member_required
def edit_office(request, id):
    office = get_object_or_404(Office, id=id)
    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            return redirect('/offices')
    else:
        form = OfficeForm(instance=office)
        return render(request, 'main/edit_office.html', {'office_form': form, 'office': office})

@staff_member_required
def delete_office(request, id):
    office = get_object_or_404(Office, id=id)
    if request.method == 'POST':
        office.delete()
        return redirect('/offices')
    return render(request, 'main/delete_office.html', {'office_form': office})


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

@staff_member_required
def add_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        
        if form.is_valid():
            print(f"End date: {form.cleaned_data['end_date']}")
            form.save()
            return redirect('sections')
    else:
        form = SectionForm()
    return render(request, 'main/add_section.html', {'section_form': form})

@staff_member_required
def edit_section(request, id):
    section = get_object_or_404(Section, id=id)
    professors = Professor.objects.all()  # Fetch all professors
    current_year = datetime.now().year
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('/sections')
    else:
        form = SectionForm(instance=section)
        return render(request, 'main/edit_section.html', {'form': form, 'section': section, 'professors': professors, 'current_year': current_year, 'course_code': course_code, 'subject': subject, 'meeting_info' : meeting_info, 'seat_capacity' : seat_capacity, 'credit' : credit, 'grading' : grading, 'requisites' : requisites, 'topic' : topic})

@staff_member_required
def delete_section(request, id):
    section = get_object_or_404(Section, id=id)
    if request.method == 'POST':
        section.delete()
        return redirect('/sections')
    return render(request, 'main/delete_section.html', {'section': section})