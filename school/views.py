from datetime import date
import uuid
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
                    print("******",school_user,"******")
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

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "school/Pages/dashboard.html")
    else:
        return redirect("/accounts/login/?redirect_to=/")


def school_info(request):
    if request.user.is_authenticated:
        school_data = sm.School.objects.get(SchoolID = request.session['school_id'])

        # year calculation
        school_date=school_data.EstDate
        today=date.today()
        school_year=today.year-school_date.year-int((today.month,today.day)<(school_date.month,school_date.day))

        context = {
            "school_data": school_data,
            "school_id": request.session['school_id'],
            "school_name": request.session['school_name'],
            "school_year":school_year,
        }
        return render(request, "school/Pages/School/school_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/SchoolInfo")


def assign_class(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)
            if request.POST.get('Class') is None:
                messages.error(request, "Please select a class")
                print("Please select a class")
            elif request.POST.get('Section') is None:
                messages.error(request, "Please select a sections")
                print("Please select a section")
            else:
                print(dict(request.POST)['Class'])
                class_list = dict(request.POST)['Class']
                section_list = dict(request.POST)['Section']

                for cl in class_list:
                    for s in section_list:
                        if not sm.AssignClass.objects.filter(Class = sm.Class.objects.get(ClassID = cl).ClassID, Section = erp.Section.objects.get(SectionID = s).SectionID, School = sm.School.objects.get(SchoolID = request.session['school_id']).SchoolID, AcademicYear = md.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID).exists():
                            if md.AcademicYear.objects.get(IsActive = True).AcademicYearID == erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID:
                                sm.AssignClass(AssignClassID = uuid.uuid4(), Class = sm.Class.objects.get(ClassID = cl), Section = erp.Section.objects.get(SectionID = s), School = sm.School.objects.get(SchoolID = request.session['school_id']), AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year'])).save()
                            else:
                                print("Please verify your academic year")

                    # Create Appplication No Details
                    if not sm.ApplicationNo.objects.filter(Class = sm.Class.objects.get(ClassID = cl).ClassID, School = sm.School.objects.get(SchoolID = request.session['school_id']).SchoolID, AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID).exists():
                        sm.ApplicationNo(ApplicationNoID = uuid.uuid4(), Class = sm.Class.objects.get(ClassID = cl), School = sm.School.objects.get(SchoolID = request.session['school_id']), AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']), Amount = 0, ApplicationNo = 1).save()

                return redirect("/School/AssignClass")
        context = {
            "ac_list": sm.AssignClass.objects.filter(AcademicYear = md.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID, School = sm.School.objects.get(SchoolID = request.session['school_id']).SchoolID).all().order_by('Class__ClassList__OrderID', 'Section__SectionName'),
            "class_list": sm.Class.objects.all().order_by('ClassList__OrderID'),
            "section_list": md.Section.objects.all().order_by('SectionName'),
            "school_name": request.session['school_name'],
            "ac_year": erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']),
        }
        return render(request, "school/Pages/School/assign_class.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/AssignClass")


def assign_application_fees(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            apf_form = fm.ApplicationFeesForm(request.POST)
            if apf_form.is_valid():
                apf_data = sm.ApplicationNo.objects.get(ApplicationNoID = apf_form.cleaned_data['ApplicationNoID'].ApplicationNoID)
                if apf_data.Amount == 0:
                    apf_data.Amount = float(apf_form.cleaned_data['Amount'])
                    apf_data.save()
                return redirect("/School/AssignApplicationFees")
            else:
                print(apf_form.errors)
        else:
            apf_form = fm.ApplicationFeesForm()
        context = {
            "apf_form": apf_form,
            "apf_list": sm.ApplicationNo.objects.filter(School = sm.School.objects.get(SchoolID = request.session['school_id']).SchoolID, AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID).all().order_by("Class__ClassList__OrderID"),
        }
        return render(request, "school/Pages/School/assign_application_fees.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/AssignApplicationFees")
