from datetime import date, datetime
import json
import os
import uuid
from django.http import HttpResponse
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
from django.db.models import Sum,Count
from num2words import num2words
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

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
                    if user.UserType == school_user:
                        login(request, user)
                        school_data = sm.School.objects.get(UserID = user)
                        request.session['school_id'] = str(school_data.SchoolID)
                        request.session['school_name'] = school_data.SchoolName
                        request.session['school_username'] = school_data.SchoolUsername
                        request.session['academic_year'] = str(school_data.CurrentAcademicYear.AcademicYearID)

                        if school_data.SchoolLogo != "":
                            school_logo=school_data.SchoolLogo.url[1:]
                            if os.path.isfile(school_logo) and os.access(school_logo,os.R_OK):
                                request.session['school_logo']="/"+str(school_data.SchoolLogo)
                                request.session['schoolimg_check']=True
                            else:
                                request.session['schoolimg_check']=False
                        else:
                            request.session['schoolimg_check']=False

                        
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
        maincls=[]
        for c in md.ClassList.objects.all().order_by("OrderID"):
            clsno=[]
            clsno.append(c.ClassName)
            clsno.append(sm.Students.objects.filter(SchoolID = request.session['school_id'],AssignedClass__Class__ClassList=c).count())
            maincls.append(clsno)

        mainfees=[]
        for c in md.ClassList.objects.all().order_by("OrderID"):
            clsfee=[]
            clsfee.append(c.ClassName)
            clsfee.append(sm.AssignFeeAmount.objects.filter(School = request.session['school_id'],Class__ClassList=c).aggregate(Sum('Amount'))['Amount__sum'])
            clsfee.append(sm.CollectFee.objects.filter(School = request.session['school_id'],AssignClass__Class__ClassList=c,PaymentStatus="Paid").count())
            clsfee.append(sm.CollectFee.objects.filter(School = request.session['school_id'],AssignClass__Class__ClassList=c,PaymentStatus="No Updates").count() + sm.CollectFee.objects.filter(School = request.session['school_id'],AssignClass__Class__ClassList=c,PaymentStatus="Pending").count())
            mainfees.append(clsfee)

        context= {
            "s_student_count": sm.Students.objects.filter(SchoolID = request.session['school_id'],AssignedClass__isnull=False).count(),
            "student_boys_count":sm.Students.objects.filter(Gender__GenderName ='Male',SchoolID = request.session['school_id'],AssignedClass__isnull=False).count(),
            "student_girls_count":sm.Students.objects.filter(Gender__GenderName ='Female',SchoolID = request.session['school_id'],AssignedClass__isnull=False).count(),
            "s_staff_count": sm.Staff.objects.filter(SchoolID = request.session['school_id']).count(),
            "male_staff_count": sm.Staff.objects.filter(SchoolID = request.session['school_id'],Gender__GenderName ='Male').count(),
            "female_staff_count": sm.Staff.objects.filter(SchoolID = request.session['school_id'],Gender__GenderName ='Female').count(),
            "cls_std":maincls,
            "cls_fees":mainfees,
        }
        return render(request, "school/Pages/dashboard.html",context)
    else:
        return redirect("/accounts/login/?redirect_to=/")

#School
def school_info(request):
    if request.user.is_authenticated:
        school_data = sm.School.objects.get(SchoolID = request.session['school_id'])
        staffhead_count=sm.SCHOOLHead.objects.filter(School = request.session['school_id']).count()
        if staffhead_count>0:
            staffhead_data=sm.SCHOOLHead.objects.filter(School = request.session['school_id']).order_by('-Staff__StaffNo')[0]
        else:
            staffhead_data=None

        # year calculation
        school_date=school_data.EstDate
        today=date.today()
        if school_data.EstDate==None:
            school_year=" "
        else:
            school_year=today.year- school_date.year-int((today.month,today.day)<(school_date.month,school_date.day))

        context = {
            "school_data": school_data,
            "staffhead_data": staffhead_data,
            "school_id": request.session['school_id'],
            "school_name": request.session['school_name'],
            "school_year":school_year,
        }
        return render(request, "school/Pages/School/school_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/SchoolInfo")

#Student
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
                    if not sm.ApplicationNo.objects.filter(Class = sm.Class.objects.get(ClassID = cl).ClassID, School = sm.School.objects.get(SchoolID = request.session['school_id']).SchoolID, 
                    AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']).AcademicYearID).exists():
                        sm.ApplicationNo(
                            ApplicationNoID = uuid.uuid4(),
                            Class = sm.Class.objects.get(ClassID = cl), 
                            School = sm.School.objects.get(SchoolID = request.session['school_id']), 
                            AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year']), 
                            Amount = 0, 
                            ApplicationNo = 1).save()

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
                messages.info(request,"Application fees saved successfully")
                return redirect("/Application/AssignApplicationFees")
            else:
                messages.error(request,apf_form.errors.as_text()[14:])
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
                messages.error(request,student_application_form.errors.as_text()[14:])
                print(student_application_form.errors)

            return redirect("/Application/NewApplication")
        else:
            application_form=fm.ApplicationForm()
            school_id = request.session['school_id']

        #creating application number autogenerate 
        if sm.Application.objects.filter(SchoolID=school_id).exists():
            old_applicationno=sm.Application.objects.filter(SchoolID=school_id).order_by('-ApplicationNo')[0].ApplicationNo
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

#Admission
def student_admission(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            student_form = fm.StudentCreateForm(request.POST)
            if student_form.is_valid():
                if sm.Students.objects.filter(AdmissionNo=request.POST.get('admission_id_no'),SchoolID = sm.School.objects.get(SchoolID = request.session['school_id'])).exists() \
                     or sm.Students.objects.filter(StudentMobileNo=student_form.cleaned_data['StudentMobileNo'],SchoolID = sm.School.objects.get(SchoolID = request.session['school_id'])).exists():
                     messages.error(request, "Applicant Already exists")
                else:
                    if request.POST.get('Application')=="":
                        applicationno=None
                    else:
                        applicationno=sm.Application.objects.get(ApplicationID=request.POST.get('Application'))

                    sm.Students(
                        AdmissionNo=request.POST.get('admission_id_no'),
                        AdmissionDate=DateFormat(date.today()).format('Y-m-d'),
                        Application=applicationno,
                        StudentName=student_form.cleaned_data['StudentName'],
                        StudentDOB=student_form.cleaned_data['StudentDOB'],
                        Gender=student_form.cleaned_data['Gender'],
                        Class=student_form.cleaned_data['Class'],
                        StudentMobileNo=student_form.cleaned_data['StudentMobileNo'],
                        FatherName=student_form.cleaned_data['FatherName'],
                        MotherName=student_form.cleaned_data['MotherName'],
                        GaurdianName=student_form.cleaned_data['GaurdianName'],
                        SchoolID=sm.School.objects.get(SchoolID = request.session['school_id']),
                        PreviousSchoolName=""
                    ).save()
                    messages.info(request,"Data saved succesfully")
                    print("Data saved succesfully")
            else:
                messages.error(request,student_form.errors.as_text()[14:])
                print(student_form.errors)

            return redirect("/Admission/NewAdmission")
        else:
            initial_data={
                "FatherName":"None",
                "MotherName":"None",
                "GaurdianName":"None",
            }
            student_form=fm.StudentCreateForm(initial=initial_data)

        school_id = request.session['school_id']
        #creating admission number autogenerate 
        if sm.Students.objects.filter(SchoolID=school_id).exists():
            old_admissionno=sm.Students.objects.filter(SchoolID=school_id).order_by('-AdmissionNo')[0].AdmissionNo
            new_admissionno="{0:03}".format(int(old_admissionno.replace(f"Adm/{date.today().year-1}-{date.today().year}/", '')) + int(1))
        else:
            new_admissionno="001"

        appobje=sm.Application.objects.filter(SchoolID=request.session['school_id'])

        no_admis_data=[]
        for ap in appobje:
            if not sm.Students.objects.filter(SchoolID=request.session['school_id'],Application=ap).exists():
                no_admis_data.append(ap)

        # passing class and fees details to javascript
        objset=sm.Application.objects.filter(SchoolID=school_id).order_by('ApplicationNo')
        jsondata=serializers.serialize("json",objset)

        context = {
            "student_form": student_form,
            "admission_id_no": f"Adm/{date.today().year-1}-{date.today().year}/{new_admissionno}",
            "amount_no":0.00,
            "admission_date": DateFormat(date.today()).format('d-m-Y'),
            "gender_list":md.Gender.objects.all().order_by('GenderOrder'),
            "application_list":no_admis_data,
            "class_list":sm.ApplicationNo.objects.filter(School=school_id),
            "student_list":sm.Students.objects.filter(SchoolID=request.session['school_id']).order_by('AdmissionNo'),
            "data":jsondata,
        }
        return render(request, "school/Pages/Admission/new_admission.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Admission/NewAdmission")

def student_info_show(request,student_id):
    if request.user.is_authenticated:
        student_data=sm.Students.objects.get(AdmissionID = student_id)
        if student_data.StudentPhoto != "":
            student_img=student_data.StudentPhoto.url[1:]
            if os.path.isfile(student_img) and os.access(student_img,os.R_OK):
                stdimg_check=os.path.isfile(student_img)
            else:
                stdimg_check=os.path.isfile(student_img)
        else:
            stdimg_check=False

        context = {
            "student":student_data,
            "stdimg_check":stdimg_check,
            "father_name":sm.Students.objects.get(AdmissionID = student_id).FatherName,
            "mother_name":sm.Students.objects.get(AdmissionID = student_id).MotherName,
            "gaurdian_name":sm.Students.objects.get(AdmissionID = student_id).GaurdianName,

        }
        return render(request, "school/Pages/Student/student_info_show.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Admission/NewAdmission")

#Staff
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
                    staff_save=sm.Staff(StaffID = uuid.uuid4(), 
                            UserID = User.objects.get(UserID = user.UserID),
                            StaffName=staff_form.cleaned_data['StaffName'], 
                            StaffEmailID=staff_form.cleaned_data['StaffEmailID'],
                            StaffMobile=staff_form.cleaned_data['StaffMobile'],
                            StaffQualification=staff_form.cleaned_data['StaffQualification'],
                            Designation=staff_form.cleaned_data['Designation'],
                            SchoolID = sm.School.objects.get(SchoolID = request.session['school_id']), 
                            StaffNo = request.POST.get('staff_id_no'),
                            Gender = staff_form.cleaned_data['Gender'],
                            )
                    staff_save.save()

                    if request.POST.get('StaffHead')!=None:
                        print('--------------',request.POST.get('StaffHead'))
                        sm.SCHOOLHead(School=sm.School.objects.get(SchoolID = request.session['school_id']),Staff=staff_save).save()

                    messages.info(request,"Record saved successfully")              
                    
                    return redirect("/Staff/CreateStaff")
            else:
                messages.error(request, staff_form.errors.as_text()[14:])
                print(staff_form.errors)
        else:
            staff_form = fm.StaffCreateForm()

        #Creating staffNo according to school
        school_id = request.session['school_id']
        if sm.Staff.objects.filter(SchoolID=school_id).exists():
            old_staffNo=sm.Staff.objects.filter(SchoolID=school_id).order_by('-StaffNo')[0].StaffNo
            new_staffNo="{0:03}".format(int(old_staffNo.replace("SCHOOL", '')) + int(1))
        else:
            new_staffNo="001"

        context = {
            "staff_form": staff_form,
            "staff_list": sm.Staff.objects.filter(SchoolID = sm.School.objects.get(SchoolID = request.session['school_id'])).all().order_by("StaffNo"),
            "designation_list":md.Designation.objects.all(),
            "staffquaify_list":md.StaffQualification.objects.all(),
            "gender_list":md.Gender.objects.all().order_by("GenderOrder"),
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

# Fees
def assign_fee_amount(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            afa_form = fm.AssignFeeAmountForm(request.POST)
            if afa_form.is_valid():
                if sm.AssignFeeAmount.objects.filter(Class = afa_form.cleaned_data['Class'], SubFee = afa_form.cleaned_data['SubFee'],School=request.session['school_id']).exists():
                    messages.error(request, "Fees already assigned")
                else:
                    sm.AssignFeeAmount(AssignFeeAmountID=uuid.uuid4(),
                    Class=afa_form.cleaned_data['Class'], 
                    FeesType=afa_form.cleaned_data['FeesType'], 
                    SubFee=afa_form.cleaned_data['SubFee'],
                    Amount=afa_form.cleaned_data['Amount'], 
                    School=sm.School.objects.get(SchoolID = request.session['school_id']), 
                    AcademicYear = erp.AcademicYear.objects.get(AcademicYearID = request.session['academic_year'])
                    ).save()
                    messages.info(request,"Fees assigned successfully")

                    return redirect("/Fees/AssignFeeAmount")
            else:
                messages.error(request, "Fees is not assigned")
                print("Something went wrong")
                print(afa_form.errors)
        else:
            afa_form = fm.AssignFeeAmountForm()
        
        # passing class and fees details to javascript
        objset=md.SubFee.objects.all()
        jsondata=serializers.serialize("json",objset)
        
        assignclass_value=sm.AssignClass.objects.filter(School=request.session['school_id']).order_by('Class__ClassList__OrderID').values_list("Class").distinct()
        # print("------------------",assignclass_value)
        classobj_value=[]
        for i in assignclass_value:
            classobj_value.append(sm.Class.objects.get(ClassID=i[0]))
            # print("-------------------",sm.Class.objects.get(ClassID=i[0]).ClassList.ClassName)
        # print(classobj_value)
        # for x in classobj_value:
        #     print("--------------",x.ClassID)
        #     print("--------------",x.ClassList.ClassName)
        
        # total_Sum=sm.AssignFeeAmount.objects.filter(Class='32d9d1dde7544f66921258935d8a8e0a').aggregate(Sum('Amount'))
        # total_Sum=sm.AssignFeeAmount.objects.filter(FeesType='').aggregate(sum('Amount'))
        # print("------------------",total_Sum) 
        
        context = {
            "afa_form": afa_form,
            "subfee_list": md.SubFee.objects.all(),
            "feetype_list": md.FeesType.objects.all(),
            "afa_list": sm.AssignFeeAmount.objects.filter(School=request.session['school_id']),
            "classobj_value":classobj_value,
            "data":jsondata,
        }
        return render(request, "school/Pages/Fees/assign_fee_amount.html", context)
    else:
        return redirect("/accounts/login/>redirect_to=/Fees/AssignFeeAmount")

def collect_fee_student(request,student_id):
    if request.user.is_authenticated:
        # student_data=None
        # attendence_form=None
        school_id = request.session['school_id']
        collect_data=sm.CollectFee.objects.get(Admission = student_id,School=school_id)

        # print("--------coole data:",collect_data)

        student_datas=sm.Students.objects.get(AdmissionID=student_id)
        totalamount=0.0
        PaidAmount=0.0
        pendingamount=0.0
        collectfee_form=fm.CollectFeeForm(request.POST)
        classobj=sm.CollectFee.objects.get(Admission=student_id).AssignClass.Class
        total_Sum=sm.AssignFeeAmount.objects.filter(Class=classobj,School=school_id).aggregate(Sum('Amount'))
        totalamount=total_Sum.get('Amount__sum')
        if request.method == 'POST':
            if collectfee_form.is_valid():           
                collect_data.ModeOfPayment=collectfee_form.cleaned_data['ModeOfPayment']
                collect_data.RefferenceNO=request.POST.get('RefferenceNO')
                if request.POST.get('Bank',False):
                    collect_data.Bank=md.Bank.objects.get(BankID=request.POST.get('Bank'))

                if request.POST.get('Online',False):
                    collect_data.Online=md.Online.objects.get(OnlineID=request.POST.get('Online'))

                collect_data.Installment=collectfee_form.cleaned_data['Installment']

                if collect_data.PaidAmount != None:
                        collect_data.PaidAmount+=collectfee_form.cleaned_data['PaidAmount']
                else:
                    collect_data.PaidAmoount=collectfee_form.cleaned_data['PaidAmount']        

                if totalamount == collect_data.PaidAmount:
                    collect_data.PaymentStatus="Paid"
                elif totalamount != collect_data.PaidAmount:
                    collect_data.PaymentStatus="Pending"
                else:
                    collect_data.PaymentStatus="No Updates"
                
                collect_data.CollectFeeNo=request.POST.get('collectfeeno')
                print("---------colle fee:",request.POST.get('collectfeeno'))
                print("---------online:",request.POST.get('Online'))
                print("---------bank:",request.POST.get('Bank'))
                collect_data.CollectFeeDate=DateFormat(date.today()).format('Y-m-d')
                collect_data.save()
                
                return redirect(f"/Fees/ShowCollectFee/{student_id}")
            else:
                print("---------------",collectfee_form.errors)
        else:
            collectfee_form = fm.CollectFeeForm(
                initial = { 
                    "ModeOfPayment": collect_data.ModeOfPayment, 
                    "RefferenceNO": collect_data.RefferenceNO,
                    "Bank": collect_data.Bank,
                    "Online": collect_data.Online,
                    "Installment": collect_data.Installment,
                    "PaidAmount": collect_data.PaidAmount,
                    "PaymentStatus": collect_data.PaymentStatus,
                    })


        if sm.CollectFee.objects.get(School=school_id,Admission=student_id).PaymentStatus=="No Updates":
            jsondata=serializers.serialize("json",md.Installment.objects.exclude(OrderID=2))
            installment_list=md.Installment.objects.exclude(OrderID=2)
            if sm.CollectFee.objects.filter(School=school_id).order_by('-CollectFeeNo')[0].CollectFeeNo!="":
                old_collectfeeno=sm.CollectFee.objects.filter(School=school_id).order_by('-CollectFeeNo')[0].CollectFeeNo 
                new_collectfeeno="{0:04}".format(int(old_collectfeeno) + int(1))
            else:
                new_collectfeeno="0001"

        elif sm.CollectFee.objects.get(School=school_id,Admission=student_id).PaymentStatus=="Pending":
            jsondata=serializers.serialize("json",md.Installment.objects.filter(OrderID=2))
            installment_list=md.Installment.objects.filter(OrderID=2)
            new_collectfeeno=sm.CollectFee.objects.get(School=school_id,Admission=student_id).CollectFeeNo
        

        pendingamount=totalamount- PaidAmount
        context = {
            "class_section_list":sm.AssignClass.objects.filter(School=request.session['school_id']).order_by('Class'),
            'student_data':student_datas,
            "collect_data":collect_data,
            "collectfeeno":new_collectfeeno,
            "collectfee_date": DateFormat(date.today()).format('d-m-Y'),
            "collectfee_form": collectfee_form,
            "installment_list":installment_list,
            "modeofpayment_list":md.ModeOfPayment.objects.all(),
            "bank_list":md.Bank.objects.all(),
            "online_list":md.Online.objects.all(),
            "collectfee_list": sm.CollectFee.objects.filter(AssignClass=request.POST.get('Class')),
            "pendingamount":pendingamount,
            "totalamount":totalamount,
            "data":jsondata
        }
        return render(request, "school/Pages/Fees/collect_fee_main.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Fees/ShowCollectFee")

def collect_fee(request):
    if request.user.is_authenticated:
        student_datas=''
        totalstudent=0
        totalamount=0.0
        PaidAmount=0.0
        pendingamount=0.0
        classobj=""
        sectionobj=""
        collectfee_form=fm.CollectFeeForm()
        if request.method == 'POST':
            if request.POST.get("form-type") == 'select-class':
                if not request.POST.get('Class')=="":
                    
                    print('1st output----------',sm.AssignClass.objects.get(AssignClassID=request.POST.get('Class')).Class.ClassList.ClassName)
                    
                    classobj=sm.AssignClass.objects.get(AssignClassID=request.POST.get('Class')).Class
                    #creating student list for attendance
                    print('---------------------------------',classobj)
                
                    sectionobj=sm.AssignClass.objects.get(AssignClassID=request.POST.get('Class')).Section
                    print("-----------------------------------",sm.AssignClass.objects.get(AssignClassID=request.POST.get('Class')).Section.SectionName)
                    
                    student_datas=sm.Students.objects.filter(AssignedClass=request.POST.get('Class')).order_by('StudentName')
                    print('2nd ouput-----------',student_datas)
                    totalstudent=student_datas.count()
                    
                    total_Sum=sm.AssignFeeAmount.objects.filter(Class=classobj,School=request.session['school_id']).aggregate(Sum('Amount'))
                    totalamount=total_Sum.get('Amount__sum')
                    print("3rd 2 amt--------------------------------",totalamount)
                    print("3rd ouput sum------------------",total_Sum)
                    
                    for i in student_datas:
                        print('6th ouput---------------------',i)
                        print('7th ouput---------------------',sm.CollectFee.objects.get(Admission=i).PaidAmount)
                        PaidAmount=sm.CollectFee.objects.get(Admission=i).PaidAmount

                else:
                    print('else-----------------',request.POST.get('Class'))
                    messages.error(request, "Please select the class")   
                    return redirect("/Fees/CollectFee") 

                if totalamount!=None:
                    if PaidAmount==totalamount:
                        pendingamount=0
                    else:
                        pendingamount=totalamount- PaidAmount
        
                # messages.error(request, "Please select the class")  
                # return redirect("/Fees/CollectFee") 
        
        context={
            # "student_data":student_data,
            "class_section_list":sm.AssignClass.objects.filter(School=request.session['school_id']).order_by('Class'),
            'student_data':student_datas,
            'total_students':totalstudent,
            "collectfee_form": collectfee_form,
            "collectfee_list": sm.CollectFee.objects.filter(AssignClass=request.POST.get('Class'),School=request.session['school_id']).order_by("Admission__StudentName"),
            "pendingamount":pendingamount,
            "totalamount":totalamount,
            "classobj":classobj,
            "sectionobj":sectionobj,            
        }
        return render(request, "school/Pages/Fees/collect_fee.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Fees/CollectFee")

def fee_info_show(request,student_id):
    if request.user.is_authenticated:
        student_id_data=sm.CollectFee.objects.get(Admission = student_id,School=request.session['school_id'])
        print("=========================",student_id_data.PaidAmount)
        ruppes=student_id_data.PaidAmount
        ruppes_in_word=num2words(ruppes)
        print("=========================",ruppes_in_word.title())
        context = {
            "student_id_data":student_id_data,
            "ruppes_in_words":ruppes_in_word.title(),
            "school_seal":sm.School.objects.get(SchoolID=request.session['school_id']).SchoolSeal,
            "school_sign":sm.School.objects.get(SchoolID=request.session['school_id']).SchoolSign,
            "school_logo":sm.School.objects.get(SchoolID=request.session['school_id']).SchoolLogo,
        }
        return render(request, "school/Pages/Fees/show_collect_fee.html", context)
        # return render(request, "school/Pages/Fees/pdf_collect_fee.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Fees/ShowCollectFee")

def mark_attendance(request):
    if request.user.is_authenticated:
        total_students=0
        student_data=None
        assign_class_data=None
        class_section_data=None
        attendance_date=None
        attendance_list=None
        report=False
        present_count=halfday_count=absent_count=0
        if request.method == 'POST':
            if request.POST.get("form-type") == 'select-class-date':
                if not request.POST.get('Class')=="":

                    #creating student list, assignedClass for attendance
                    attendance_date=request.POST.get('AttendanceDate')
                    assign_class_data= request.POST.get('Class')
                    school_id = request.session['school_id']
                    if sm.Attendance.objects.filter(AttendanceDate=attendance_date,AssignClass=assign_class_data,SchoolID =school_id).exists():
                        attendance_list=sm.Attendance.objects.filter(AttendanceDate=attendance_date,AssignClass=assign_class_data,SchoolID =school_id).order_by('StudentID__StudentName')
                        total_students=attendance_list.count()
                        report=True
                        present_count=sm.Attendance.objects.filter(AttendanceDate=attendance_date,AssignClass=assign_class_data,AttendanceMark='Present',SchoolID =school_id).count()
                        halfday_count=sm.Attendance.objects.filter(AttendanceDate=attendance_date,AssignClass=assign_class_data,AttendanceMark='Half Day',SchoolID =school_id).count()
                        absent_count=sm.Attendance.objects.filter(AttendanceDate=attendance_date,AssignClass=assign_class_data,AttendanceMark='Absent',SchoolID =school_id).count()
                    else:
                        student_data=sm.Students.objects.filter(AssignedClass=request.POST.get('Class'),SchoolID =school_id).order_by('StudentName')
                        total_students=student_data.count()

                    class_section_data=sm.AssignClass.objects.get(AssignClassID=assign_class_data,School=school_id)

                    
                else:
                    messages.error(request, "Please select the class")           

            if request.POST.get("form-type")=='mark-attendance':
                school_id = request.session['school_id']
                student_data=sm.Students.objects.filter(AssignedClass=request.POST.get('assign_class_id'),SchoolID =school_id).order_by('StudentName')
                attendance_date=request.POST.get('attendance_date')
                assign_class_data=request.POST.get('assign_class_id')

                if sm.Attendance.objects.filter(AttendanceDate=attendance_date,AssignClass=assign_class_data,SchoolID =school_id).exists():
                    messages.error(request, "Attendance is already marked for that day for that class")           
                else:
                    for atst in student_data:
                        sm.Attendance(
                            StudentID=atst,
                            AttendanceDate=attendance_date,
                            AssignClass=sm.AssignClass.objects.get(AssignClassID=assign_class_data,School =school_id),
                            AttendanceMark=request.POST.get(f'choice-{atst.AdmissionID }'),
                            SchoolID = sm.School.objects.get(SchoolID = request.session['school_id']), 
                        ).save()
                    messages.info(request,"Student Attendace saved successfully")
                return redirect("/Attendance/MarkAttendance")

        context={
            "student_data":student_data,
            "total_students":total_students,
            "assign_class_data":assign_class_data,
            "class_section_data":class_section_data,
            "attendance_date":attendance_date,
            "class_section_list":sm.AssignClass.objects.filter(School=request.session['school_id']).order_by('Class'),
            "report":report,
            "present_count":present_count,
            "halfday_count":halfday_count,
            "absent_count":absent_count,
            "attendance_list":attendance_list,
        }
        return render(request, "school/Pages/Attendance/mark_attendance.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Attendance/MarkAttendance")

def attendance_list(request):
    if request.user.is_authenticated:

        student_data=None
        total_students=0
        class_section_data=None

        if request.method == 'POST':            
            class_id=request.POST['class_selected']
            if not class_id=='':
                student_data=sm.Students.objects.filter(SchoolID=request.session['school_id'],AssignedClass = class_id).order_by('StudentName')
                total_students=student_data.count()
                class_section_data=sm.AssignClass.objects.get(AssignClassID=class_id,School=request.session['school_id'])
            else:
                messages.error(request, "Please select the class")       
                return redirect("/Attendance/ReportAttendance")


        assignclass_list = sm.AssignClass.objects.filter(School=request.session['school_id']).order_by('Class')
        context = {
            "assignclass_list": assignclass_list,
            "student_data":student_data,
            "total_students":total_students,
            "class_section_data":class_section_data,
        }
        return render(request, "school/Pages/Attendance/attendance_student_list.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Attendance/ReportAttendance")

def student_attendance_show(request,student_id):
    if request.user.is_authenticated:
        school_id=request.session['school_id']
        student_data=sm.Students.objects.get(AdmissionID = student_id,SchoolID=school_id)
        if student_data.StudentPhoto != "":
            student_img=student_data.StudentPhoto.url[1:]
            if os.path.isfile(student_img) and os.access(student_img,os.R_OK):
                stdimg_check=os.path.isfile(student_img)
            else:
                stdimg_check=os.path.isfile(student_img)
        else:
            stdimg_check=False

        total_present=sm.Attendance.objects.filter(StudentID=student_id,SchoolID=school_id,AttendanceMark='Present').count()
        total_halfday=sm.Attendance.objects.filter(StudentID=student_id,SchoolID=school_id,AttendanceMark='Half Day').count()
        total_absent=sm.Attendance.objects.filter(StudentID=student_id,SchoolID=school_id,AttendanceMark='Absent').count()
        student_attendance=sm.Attendance.objects.filter(StudentID=student_id,SchoolID=school_id)
        total_attendance=student_attendance.count()

        jsondata=serializers.serialize("json",student_attendance)

        context = {
            "student_data":student_data,
            "total_present":total_present,
            "total_halfday":total_halfday,
            "total_absent":total_absent, 
            "total_attendance":total_attendance, 
            "data":jsondata,
            "stdimg_check":stdimg_check,
        }
        return render(request, "school/Pages/Attendance/student_attendance_show.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Attendance/ReportAttendance")

def feedback_info(request):
    if request.user.is_authenticated:
        if request.method == 'POST':     
            feedback=md.Feedback()
            schooldata=sm.School.objects.get(SchoolID=request.session['school_id'])
            schoolname=schooldata.SchoolName
            schoolDISECode=schooldata.SchoolDISECode

            feedback.FeedbackData=request.POST.get("feedback_data") 
            if request.FILES.get('feedback_file',False):
                feedback.FeedbackFile=request.FILES.get('feedback_file')
            feedback.School=f"{schoolname} {schoolDISECode}"
            feedback.save()
            messages.info(request, "Feedback sent successfully")           

        return render(request, "school/Pages/Feedback/school_feedback.html")
    else:
        return redirect("/accounts/login/?redirect_to=/Feedback/FeedbackInfo")


# Delete Information functions

def delete_staff(request,staff_id):
    if request.user.is_authenticated:
        staff_data=sm.Staff.objects.get(StaffID = staff_id)
        user_data=User.objects.get(UserID=staff_data.UserID.UserID)
        staff_data.delete()
        user_data.delete()
        messages.info(request,"Record deleted successfully")              
        return redirect("/Staff/CreateStaff")
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/CreateStaff")

def delete_student(request,student_id):
    if request.user.is_authenticated:
        student_data=sm.Students.objects.get(AdmissionID = student_id)
        
        if student_data.Application:
            print("----------app:",student_data.Application.ApplicationID)
            application_data=sm.Application.objects.get(ApplicationID=student_data.Application.ApplicationID)
            application_data.delete()

        student_data.delete()
        messages.info(request,"Student record deleted successfully")              
        return redirect("/Admission/NewAdmission")
    else:
        return redirect("/accounts/login/?redirect_to=/Admission/NewAdmission")

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    return HttpResponse(result.getvalue(), content_type='application/pdf')


def fees_reciept_pdf(request,student_id):
    if request.user.is_authenticated:
        student_id_data=sm.CollectFee.objects.get(Admission = student_id,School=request.session['school_id'])
        ruppes=student_id_data.PaidAmount
        ruppes_in_word=num2words(ruppes)
        context = {
            "student_id_data":student_id_data,
            "ruppes_in_words":ruppes_in_word.title(),
            "school_seal":sm.School.objects.get(SchoolID=request.session['school_id']).SchoolSeal,
            "school_sign":sm.School.objects.get(SchoolID=request.session['school_id']).SchoolSign,
            "school_logo":sm.School.objects.get(SchoolID=request.session['school_id']).SchoolLogo,
        }
        pdf=render_to_pdf("school/Pages/Fees/pdf_collect_fee.html", context)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename=f"{student_id_data.Admission.StudentName}_{student_id_data.CollectFeeNo}.pdf"
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return redirect("/accounts/login/?redirect_to=/Fees/ShowCollectFee")
