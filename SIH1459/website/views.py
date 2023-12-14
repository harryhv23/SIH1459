from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import State, Scheme, Course, College
from .forms import AddSchemeForm, AddCourseForm, AddCollegeForm, AddStudentForm, SearchStudentForm


# Create your views here.
def home(request):
    # check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('home')
        else:
            messages.success(request, 'ERROR! Invalid Credential')
            return redirect('home')
    else:
        return render(request, 'home.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been Logged Out...')
    return redirect('home')


def student_page(request):
    if request.user.is_authenticated:
        return render(request, 'student_page.html', {})
    else:
        messages.success(request, 'Please log in first')
        return redirect('home')


def courses_page(request):
    course_records = Course.objects.all()
    if request.user.is_authenticated:
        return render(request, 'courses_page.html', {'course_records': course_records})
    else:
        messages.success(request, 'Please log in first')
        return redirect('home')


def courses_search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            search_by = request.POST.get('search_by')
            courses_search = request.POST.get('courses_search')
            if courses_search:
                if search_by == 'course_code':
                    result_search = Course.objects.filter(code__icontains=courses_search)
                    return render(request, 'courses_search.html', {'result_search': result_search})
                elif search_by == 'course_name':
                    # result_search = Course.objects.raw(f"SELECT * FROM website_course WHERE name ='{searched_for}' ")
                    result_search = Course.objects.filter(name__icontains=courses_search)
                    return render(request, 'courses_search.html', {'result_search': result_search})
                else:
                    messages.success(request, 'Please enter a valid scheme id')
                    return redirect('courses_page')
            else:
                messages.success(request, 'Please enter a valid scheme id')
                return redirect('courses_page')
        else:
            return redirect('courses_page')
    else:
        messages.success(request, 'You must be logged in ')
        return redirect('home')


def schemes_page(request):
    scheme_records = Scheme.objects.all()
    if request.user.is_authenticated:
        return render(request, 'schemes_page.html', {'scheme_records': scheme_records})
    else:
        messages.success(request, 'Please log in first')
        return redirect("home")


def schemes_search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            search_by = request.POST.get('search_by')
            scheme_search = request.POST.get('scheme_search')
            if scheme_search:
                if search_by == 'scheme_id':
                    result_search = Scheme.objects.filter(id__icontains=scheme_search)
                    return render(request, 'schemes_search.html', {'result_search': result_search})
                elif search_by == 'scheme_name':
                    # result_search = Course.objects.raw(f"SELECT * FROM website_course WHERE name ='{searched_for}' ")
                    result_search = Scheme.objects.filter(name__icontains=scheme_search)
                    return render(request, 'schemes_search.html', {'result_search': result_search})
                else:
                    messages.success(request, 'Please enter a valid scheme id')
                    return redirect('schemes_page')
            else:
                messages.success(request, 'Please enter a valid scheme id')
                return redirect('schemes_page')
        else:
            return redirect('schemes_page')
    else:
        messages.success(request, 'You must be logged in ')
        return redirect('home')


def state_page(request):
    state_records = State.objects.all()
    if request.user.is_authenticated:
        return render(request, 'state_page.html', {'state_records': state_records})
    else:
        messages.success(request, 'Please log in first')
        return redirect("home")


def college_page(request):
    college_records = College.objects.all()
    if request.user.is_authenticated:
        return render(request, 'college_page.html', {'college_records': college_records})
    else:
        messages.success(request, 'Please log in first')
        return redirect("home")


def add_college(request):
    form = AddCollegeForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'College Added')
                return redirect('college_page')
        return render(request, 'add_college.html', {'form': form})
    else:
        messages.success(request, 'You must be loggedin')
        return redirect('home')


def add_student(request):
    form = AddStudentForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Student Added')
                return redirect('student_page')
        return render(request, 'add_student.html', {'form': form})
    else:
        messages.success(request, 'You must be loggedin')
        return redirect('home')


def add_scheme(request):
    form = AddSchemeForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Scheme Added')
                return redirect('schemes_page')
        return render(request, 'add_scheme.html', {'form': form})
    else:
        messages.success(request, 'You must be loggedin')
        return redirect('home')


def add_course(request):
    form = AddCourseForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Course Added')
                return redirect('courses_page')
        return render(request, 'add_course.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in')
        return redirect('home')


# def student_search(request):
#     form = SearchStudentForm(request.POST or None)
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             if form.is_valid():
#                 form.save()
#                 render(request, 'student_search.html', {'result_search': form})
#             return render(request, 'student_page.html', {'form': form})
#         return redirect('student_page')
#     else:
#         messages.success(request, 'You must be logged in')
#         return redirect('home')

def student_page(request):
    form = SearchStudentForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                return render(request, 'student_search.html', {'form': form})
        return render(request, 'student_page.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in')
        return redirect('home')
