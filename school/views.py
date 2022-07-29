from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from school import forms as fm
from dshiksha_erp import models as md
from school import models as sm
from main.models import UserTypes, User
import dshiksha_erp.models as erp


# Create your views here.

# def index(request):
#     return render(request,'school/index.html')

# def login_view(request):
#     return render(request,'school/login.html')

def index(request):
    if request.user.is_authenticated:
        return redirect("/Dashboard")
    else:
        return redirect("/accounts/login/?redirect_to=/")

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            redirect_url = ""
            login_form = fm.LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(request, username = login_form.cleaned_data['Email'], password = login_form.cleaned_data['Password'])
                if user is None:
                    messages.error(request, "Invalid credentials")
                    return redirect("/accounts/login/?=redirect_to="+login_form.data['redirect_to_url'])
                else:
                    school_user = UserTypes.objects.get(UserTypeName = 'SCHOOL')
                    # print("******",school_user,"******")
                    if user.UserType == school_user:
                        login(request, user)
                        school_data = sm.School.objects.get(UserID = user)
                        request.session['school_id'] = str(school_data.SchoolID)
                        request.session['school_name'] = school_data.SchoolName
                        request.session['school_username'] = school_data.SchoolUsername
                        request.session['academic_year'] = str(school_data.CurrentAcademicYear.AcademicYearID)
                        return redirect(login_form.data['redirect_to_url'])
                    else:
                        messages.error(request, "You donot have permission to access this page")
                        return redirect("/accounts/login/?redirect_to="+login_form.data['redirect_to_url'])
            else:
                messages.error(request, "You donot have permission to access this page")
                print(login_form.errors)
                return redirect("/accounts/login/?redirect_to="+login_form.data['redirect_to_url'])
        else:
            if request.GET.get('redirect_to') is None:
                redirect_url = "/"
            else:
                redirect_url = request.GET.get('redirect_to')
            login_form = fm.LoginForm()
        context = {
            "login_form": login_form,
            "redirect_url": redirect_url,
        }
        return render(request, "school/login.html", context)
    else:
        return redirect("/Dashboard")

def logout_view(request):
    request.session.clear()
    logout(request)
    return redirect('login?redirect_to=/')
