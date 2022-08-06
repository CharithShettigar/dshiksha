from datetime import date, datetime
import uuid
from django.utils.dateformat import DateFormat
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from school import forms as fm
from dshiksha_erp import models as md
from school import models as sm
from main.models import UserTypes, User
import dshiksha_erp.models as erp
from django.core import serializers

# Create your views here.


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
                            # if md.AcademicYear.objects.get(IsActive = True).AcademicYearID == erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID:
                            sm.AssignClass(AssignClassID = uuid.uuid4(), Class = sm.Class.objects.get(ClassID = cl), Section = erp.Section.objects.get(SectionID = s), School = sm.School.objects.get(SchoolID = request.session['school_id']), AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year'])).save()
                            # else:
                                # print("Please verify your academic year")

                    #Create Appplication No Details
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
                # if apf_data.Amount == 0:
                apf_data.Amount = float(apf_form.cleaned_data['Amount'])
                apf_data.save()
                return redirect("/Application/AssignApplicationFees")
            else:
                print(apf_form.errors)
        else:
            apf_form = fm.ApplicationFeesForm()
        context = {
            "apf_form": apf_form,
            "apf_list": sm.ApplicationNo.objects.filter(School = sm.School.objects.get(SchoolID = request.session['school_id']).SchoolID, AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID).all().order_by("Class__ClassList__OrderID"),
        }
        return render(request, "school/Pages/Application/assign_application_fees.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Application/AssignApplicationFees")

def student_application(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            student_application_form = fm.ApplicationForm(request.POST)
            if student_application_form.is_valid():
                if sm.Application.objects.filter(ApplicationNo=request.POST.get('application_id_no'),SchoolID = sm.School.objects.get(SchoolID = request.session['school_id'])).exists() \
                    or sm.Application.objects.filter(StudentMobileNo=student_application_form.cleaned_data['StudentMobileNo'],SchoolID = sm.School.objects.get(SchoolID = request.session['school_id'])).exists():
                    messages.error(request, "Applicant Already exists")
                else:
                    sm.Application(
                        ApplicationID=uuid.uuid4(),
                        ApplicationNo=request.POST.get('application_id_no'),
                        StudentName=student_application_form.cleaned_data['StudentName'],
                        StudentDOB=student_application_form.cleaned_data['StudentDOB'],
                        # Gender=md.Gender.objects.get(GenderID=student_application_form.cleaned_data['Gender']),
                        Gender=student_application_form.cleaned_data['Gender'],
                        StudentMobileNo=student_application_form.cleaned_data['StudentMobileNo'],
                        ParentName=student_application_form.cleaned_data['ParentName'],
                        ParentMobileNo=student_application_form.cleaned_data['ParentMobileNo'],
                        Class=student_application_form.cleaned_data['Class'],
                        SchoolID=sm.School.objects.get(SchoolID = request.session['school_id']),
                        ApplicationDate=DateFormat(date.today()).format('Y-m-d'),
                        Amount=student_application_form.cleaned_data['Amount'],
                        ModeOfPayment=student_application_form.cleaned_data['ModeOfPayment']
                        # ModeOfPayment=md.ModeOfPayment.objects.get(ModeOfPaymentID=student_application_form.cleaned_data['ModeOfPayment'])
                    ).save()
                    messages.info(request,"Data saved succesfully")
                    print("Data saved succesfully")
            else:
                print(student_application_form.errors)

            return redirect("/Application/NewApplication")

        else:
            application_form=fm.ApplicationForm()
            school_id = request.session['school_id']

            #creating application number autogenerate 
            if sm.Application.objects.filter(SchoolID=school_id).exists():
                old_applicationno=sm.Application.objects.filter(SchoolID=school_id)[0].ApplicationNo
                new_applicationno="{0:03}".format(int(old_applicationno.replace(f"A/{date.today().year-1}-{date.today().year}/", '')) + int(1))
            else:
                new_applicationno="001"

            # passing class and fees details to javascript
            objset=sm.ApplicationNo.objects.filter(School=school_id)
            jsondata=serializers.serialize("json",objset)

        context = {
            "application_form": application_form,
            "application_id_no": f"A/{date.today().year-1}-{date.today().year}/{new_applicationno}",
            "amount_no":0.00,
            "application_date": DateFormat(date.today()).format('d-m-Y'),
            "gender_list":md.Gender.objects.all().order_by('GenderOrder'),
            "class_list":objset,
            "payment_list":md.ModeOfPayment.objects.all(),
            "applicant_list":sm.Application.objects.filter(SchoolID=request.session['school_id']).order_by('ApplicationNo'),
            "data":jsondata,
        }
        return render(request, "school/Pages/Application/new_application.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Application/NewApplication")

def application_info_show(request,application_ID):
    if request.user.is_authenticated:
        application_ID_data=sm.Application.objects.get(ApplicationID = application_ID)
        context = {
            "applicant":application_ID_data,
        }
        return render(request, "school/Pages/Application/application_info_show.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Application/NewApplication")

def create_staff(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            staff_form = fm.StaffCreateForm(request.POST)
            if staff_form.is_valid():
                if sm.Staff.objects.filter(StaffEmailID = staff_form.cleaned_data['StaffEmailID'],
                                            SchoolID = sm.School.objects.get(SchoolID = request.session[
                                                'school_id'])).exists() \
                        or \
                        sm.Staff.objects.filter(StaffMobile = staff_form.cleaned_data['StaffMobile'],
                                                 SchoolID = sm.School.objects.get(SchoolID =
                                                                                   request.session[
                                                                                       'school_id'])).exists():
                    messages.error(request, "Staff Already exists")
                else:
                    user = User.objects.create_user(email=staff_form.cleaned_data['StaffEmailID'],
                                                    username=staff_form.cleaned_data['StaffName'],
                                                    first_name=staff_form.cleaned_data['StaffName'],
                                                    password=staff_form.cleaned_data['Password'],
                                                    UserType=UserTypes.objects.get(UserTypeName = "SCHOOL Staff").UserTypeID,
                                                    )
                    sm.Staff(StaffID = uuid.uuid4(), 
                            UserID = User.objects.get(UserID = user.UserID),
                            StaffName=staff_form.cleaned_data['StaffName'], 
                            StaffEmailID=staff_form.cleaned_data['StaffEmailID'],
                            StaffMobile=staff_form.cleaned_data['StaffMobile'], 
                            SchoolID = sm.School.objects.get(SchoolID = request.session['school_id']), 
                            StaffNo = request.POST.get('staff_id_no'),
                            ).save()
                    
                    return redirect("/Staff/CreateStaff")
            else:
                messages.error(request, staff_form.errors.as_text()[14:])              
                print(staff_form.errors)
        else:
            staff_form = fm.StaffCreateForm()

            #Creating staffNo according to school
            school_id = request.session['school_id']
            if sm.Staff.objects.filter(SchoolID=school_id).exists():
                old_staffNo=sm.Staff.objects.filter(SchoolID=school_id)[0].StaffNo
                new_staffNo="{0:03}".format(int(old_staffNo.replace("SCHOOL", '')) + int(1))
            else:
                new_staffNo="001"

        context = {
            "staff_form": staff_form,
            "staff_list": sm.Staff.objects.filter(SchoolID = sm.School.objects.get(SchoolID = request.session['school_id'])).all().order_by("StaffNo"),
            "staff_id_no": "SCHOOL" +new_staffNo,            
        }
        return render(request, "school/Pages/Staff/create_staff.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/CreateStaff")

def staff_info(request):
    if request.user.is_authenticated:

        staff_data=None
        if request.method == 'POST':            
            staff_id=request.POST['staff_selected']
            if not staff_id=='':
                staff_data=sm.Staff.objects.get(StaffID = staff_id)

        staff_list = sm.Staff.objects.filter(SchoolID=request.session['school_id'])
        context = {
            "staff_list": staff_list,
            "staff":staff_data,
        }
        return render(request, "school/Pages/Staff/staff_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/StaffInfo")

def staff_info_show(request,staff_ID):
    if request.user.is_authenticated:
        staff_data=sm.Staff.objects.get(StaffID = staff_ID)
        context = {
            "staff":staff_data,
        }
        return render(request, "school/Pages/Staff/staff_info_show.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/StaffInfo")