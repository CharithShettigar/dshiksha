from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from school import forms as fm
from dshiksha_erp import models as md
from school import models as sm
from main.models import UserTypes, User
import dshiksha_erp.models as erp
from django.core import serializers
import os
import uuid

# Update View methods

def update_school(request, school_id):
    if request.user.is_authenticated:
        school_data = sm.School.objects.get(SchoolID = school_id)

        if request.method == "POST":
            school_form = fm.SchoolForm(request.POST)
            if school_form.is_valid():
                school_data.SchoolDISECode=school_form.cleaned_data['SchoolDISECode']
                school_data.SyllabusType=school_form.cleaned_data['SyllabusType']
                school_data.InsitutionLevel=school_form.cleaned_data['InsitutionLevel']
                school_data.CurrentAcademicYear=school_form.cleaned_data['CurrentAcademicYear']

                if request.FILES.get('school_img',False):
                    if school_data.SchoolLogo != "":
                        os.remove(school_data.SchoolLogo.path)
                    school_data.SchoolLogo=request.FILES['school_img']

                if request.FILES.get('schoolseal_img',False):
                    if school_data.SchoolSeal != "":
                        os.remove(school_data.SchoolSeal.path)
                    school_data.SchoolSeal=request.FILES['schoolseal_img']

                if request.FILES.get('schoolsign_img',False):
                    if school_data.SchoolSign != "":
                        os.remove(school_data.SchoolSign.path)
                    school_data.SchoolSign=request.FILES['schoolsign_img']

                school_data.Landline=school_form.cleaned_data['Landline']
                school_data.Mobile=school_form.cleaned_data['Mobile']
                school_data.Website=school_form.cleaned_data['Website']
                school_data.EstDate=school_form.cleaned_data['EstDate']
                school_data.History=school_form.cleaned_data['History']
                school_data.SchoolPANNo=school_form.cleaned_data['SchoolPANNo']
                school_data.GSTINo=school_form.cleaned_data['GSTINo']
                school_data.Area=school_form.cleaned_data['Area']
                school_data.Village=school_form.cleaned_data['Village']
                school_data.Pincode=school_form.cleaned_data['Pincode']
                school_data.AccountantName=school_form.cleaned_data['AccountantName']
                school_data.AccountantEmail=school_form.cleaned_data['AccountantEmail']
                school_data.AccountantMobile=school_form.cleaned_data['AccountantMobile']
                school_data.AccountantWhatsAppNo=school_form.cleaned_data['AccountantWhatsAppNo']
                school_data.CorrespondentName=school_form.cleaned_data['CorrespondentName']
                school_data.CorrespondentEmail=school_form.cleaned_data['CorrespondentEmail']
                school_data.CorrespondentMobile=school_form.cleaned_data['CorrespondentMobile']
                school_data.CorrespondentWhatsAppNo=school_form.cleaned_data['CorrespondentWhatsAppNo']
                school_data.save()
                messages.info(request,"Staff information updated successfully")
                return redirect(f"/Update/UpdateSchoolInfo/{school_id}")
            else:
                messages.error(request,f"Wrong information entererd!!! {school_form.errors}")
                print("---------------",school_form.errors)
        else:
            school_form = fm.SchoolForm(
                initial = { 
                    "SchoolName": school_data.SchoolName, 
                    # "SchoolCode": school_data.SchoolCode,
                    "SchoolDISECode": school_data.SchoolDISECode,
                    "SchoolType": school_data.SchoolType,
                    "Landline": school_data.Landline,
                    "Mobile": school_data.Mobile,
                    # "Email": school_data.Email,
                    "Website": school_data.Website,
                    "EstDate": school_data.EstDate,
                    "History": school_data.History,
                    "SchoolPANNo": school_data.SchoolPANNo,
                    "GSTINo": school_data.GSTINo,
                    # "SchoolCode": school_data.SchoolCode,
                    # "SchoolUsername": school_data.SchoolUsername,
                    "SyllabusType": school_data.SyllabusType,

                    "AccountantName": school_data.AccountantName,
                    "AccountantEmail": school_data.AccountantEmail,
                    "AccountantMobile": school_data.AccountantMobile,
                    "AccountantWhatsAppNo": school_data.AccountantWhatsAppNo,

                    "CorrespondentName": school_data.CorrespondentName,
                    "CorrespondentEmail": school_data.CorrespondentEmail,
                    "CorrespondentMobile": school_data.CorrespondentMobile,
                    "CorrespondentWhatsAppNo": school_data.CorrespondentWhatsAppNo,
                    })

        context = {
            "school_data": school_data,
            "school_form": school_form,
            "village_list":md.Village.objects.all(),
            "currentacademicYear_list":md.AcademicYear.objects.all(),
            "postoffice_list":md.PostOffice.objects.all(),
            "area_list":md.Area.objects.all(),
            "institution_list":md.InstitutionLevel.objects.all(),
            "school_id": request.session['school_id'],
            "school_logo":school_data.SchoolLogo,
            "school_seal":school_data.SchoolSeal,
            "school_sign":school_data.SchoolSign,
            "Email":school_data.Email
        }
        return render(request, "school/Pages/Update/update_school_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/SchoolInfo")


def update_staff(request, staff_id):
    if request.user.is_authenticated:
        staff_data = sm.Staff.objects.get(StaffID = staff_id)

        if request.method == "POST":
            staff_form = fm.StaffForm(request.POST)
            if staff_form.is_valid():
                staff_data.StaffName=staff_form.cleaned_data['StaffName']
                staff_data.StaffEmailID= staff_form.cleaned_data['StaffEmailID']
                staff_data.StaffMobile= staff_form.cleaned_data['StaffMobile']

                if request.FILES.get('staff_img',False):
                    if staff_data.StaffPhoto != "":
                        os.remove(staff_data.StaffPhoto.path)
                    staff_data.StaffPhoto=request.FILES['staff_img']
                
                staff_data.Gender= staff_form.cleaned_data['Gender']
                staff_data.DOB= staff_form.cleaned_data['DOB']
                staff_data.BloodGroup= staff_form.cleaned_data['BloodGroup']
                staff_data.MaritalStatus= staff_form.cleaned_data['MaritalStatus']
                staff_data.Caste= staff_form.cleaned_data['Caste']
                staff_data.MotherTongue= staff_form.cleaned_data['MotherTongue']
                staff_data.AddressLine1= staff_form.cleaned_data['AddressLine1']
                staff_data.AddressLine2= staff_form.cleaned_data['AddressLine2']
                staff_data.Village= staff_form.cleaned_data['Village']
                staff_data.Pincode= staff_form.cleaned_data['Pincode']
                staff_data.StaffWhatsAppNo= staff_form.cleaned_data['StaffWhatsAppNo']
                staff_data.Designation= staff_form.cleaned_data['Designation']
                staff_data.StaffQualification= staff_form.cleaned_data['StaffQualification']
                staff_data.Subject1= staff_form.cleaned_data['Subject1']
                staff_data.Subject2= staff_form.cleaned_data['Subject2']
                staff_data.DateOfAppointment=staff_form.cleaned_data['DateOfAppointment']
                staff_data.DateOfRetirement= staff_form.cleaned_data['DateOfRetirement']
                staff_data.AcademicYear= staff_form.cleaned_data['AcademicYear']
                staff_data.save()
                messages.info(request,"Staff information updated successfully")
                return redirect(f"/Update/UpdateStaffInfo/{staff_id}")
            else:
                messages.error(request,f"Wrong information entererd!!! {staff_form.errors}")
                print("---------------",staff_form.errors)
        else:
            staff_form = fm.StaffForm(
                initial = { 
                    "StaffName": staff_data.StaffName, 
                    "StaffEmailID" : staff_data.StaffEmailID,
                    "StaffMobile": staff_data.StaffMobile,
                    "DOB": staff_data.DOB,
                    "AddressLine1": staff_data.AddressLine1,
                    "AddressLine2": staff_data.AddressLine2,
                    "StaffWhatsAppNo": staff_data.StaffWhatsAppNo,
                    "DateOfAppointment": staff_data.DateOfAppointment,
                    "DateOfRetirement": staff_data.DateOfRetirement,
                    })

        context = {
            "staff_form": staff_form,
            "gender_list":md.Gender.objects.all(),
            "bloodgroup_list":md.BloodGroup.objects.all(),
            "maritalstatus_list":md.MaritalStatus.objects.all(),
            "caste_list":md.Caste.objects.all(),
            "mothertongue_list":md.MotherTongue.objects.all(),
            "village_list":md.Village.objects.all(),
            "postoffice_list":md.PostOffice.objects.all(),
            "designation_list":md.Designation.objects.all(),
            "staffqualification_list":md.StaffQualification.objects.all(),
            "staffsubject_list":md.StaffSubject.objects.all(),
            "currentacademicYear_list":md.AcademicYear.objects.all(),
            "staff_data": staff_data,
            "staff_photo":staff_data.StaffPhoto,
        }
        return render(request, "school/Pages/Update/update_staff_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/StaffInfo")


def update_student(request, student_id):
    if request.user.is_authenticated:
        school_id=request.session['school_id']
        student_data = sm.Students.objects.get(SchoolID=school_id,AdmissionID = student_id)
        if request.method == "POST":
            student_form = fm.StudentForm(request.POST)
            if student_form.is_valid():
                student_data.StudentName=student_form.cleaned_data['StudentName']
                student_data.StudentDOB=student_form.cleaned_data['StudentDOB']
                student_data.Gender=student_form.cleaned_data['Gender']
                student_data.StudentMobileNo=student_form.cleaned_data['StudentMobileNo']

                if request.FILES.get('student_img',False):
                    if student_data.StudentPhoto != "":
                        os.remove(student_data.StudentPhoto.path)
                    student_data.StudentPhoto=request.FILES['student_img']

                student_data.Village=student_form.cleaned_data['Village']
                student_data.Nationality=student_form.cleaned_data['Nationality']
                student_data.BloodGroup=student_form.cleaned_data['BloodGroup']
                student_data.Religion=student_form.cleaned_data['Religion']
                student_data.CasteCategory=student_form.cleaned_data['CasteCategory']
                student_data.PreviousSchoolName=student_form.cleaned_data['PreviousSchoolName']
                student_data.MotherTongue=student_form.cleaned_data['MotherTongue']
                student_data.Caste=student_form.cleaned_data['Caste']
                student_data.AddressLine1=student_form.cleaned_data['AddressLine1']
                student_data.AddressLine2=student_form.cleaned_data['AddressLine2']
                student_data.Village=student_form.cleaned_data['Village']
                student_data.Pincode=student_form.cleaned_data['Pincode']
                student_data.Class=student_form.cleaned_data['Class']
                student_data.AssignedClass=student_form.cleaned_data['AssignedClass']

                if student_data.FatherName == None or student_data.FatherName == "None":
                    student_data.FatherName="None"
                else:
                    student_data.FatherName=student_form.cleaned_data['FatherName']

                student_data.FatherMobileNo=student_form.cleaned_data['FatherMobileNo']
                student_data.FatherWhatsappNo=student_form.cleaned_data['FatherWhatsappNo']
                student_data.FatherEmail=student_form.cleaned_data['FatherEmail']
                student_data.FatherQualification=student_form.cleaned_data['FatherQualification']
                student_data.FatherOccupation=student_form.cleaned_data['FatherOccupation']
                student_data.FatherIncome=student_form.cleaned_data['FatherIncome']

                if student_data.MotherName == None or student_data.MotherName == "None":
                    student_data.MotherName="None"
                else:
                    student_data.MotherName=student_form.cleaned_data['MotherName']

                student_data.MotherMobileNo=student_form.cleaned_data['MotherMobileNo']
                student_data.MotherWhatsappNo=student_form.cleaned_data['MotherWhatsappNo']
                student_data.MotherEmail=student_form.cleaned_data['MotherEmail']
                student_data.MotherQualification=student_form.cleaned_data['MotherQualification']
                student_data.MotherOccupation=student_form.cleaned_data['MotherOccupation']
                student_data.MotherIncome=student_form.cleaned_data['MotherIncome']

                if student_data.GaurdianName == None or student_data.GaurdianName == "None":
                    student_data.GaurdianName="None"
                else:
                    student_data.GaurdianName=student_form.cleaned_data['GaurdianName']

                student_data.GaurdianMobileNo=student_form.cleaned_data['GaurdianMobileNo']
                student_data.GaurdianWhatsappNo=student_form.cleaned_data['GaurdianWhatsappNo']
                student_data.GaurdianEmail=student_form.cleaned_data['GaurdianEmail']
                student_data.GaurdianQualification=student_form.cleaned_data['GaurdianQualification']
                student_data.GaurdianOccupation=student_form.cleaned_data['GaurdianOccupation']
                student_data.GaurdianIncome=student_form.cleaned_data['GaurdianIncome']
                student_data.save()
                
                if not sm.CollectFee.objects.filter(Admission=student_id, School = sm.School.objects.get(SchoolID = request.session['school_id']).SchoolID).exists():
                    sm.CollectFee(
                        CollectFeeID=uuid.uuid4(),
                        Admission=sm.Students.objects.get(AdmissionID=student_id), 
                        AssignClass=student_data.AssignedClass,                        
                        School=sm.School.objects.get(SchoolID = request.session['school_id']),
                        PaymentStatus="No Updates",
                        PaidAmount=0
                        ).save()
                # else:
                #     print("alredy created")
                # # print('1st-----------------------',sm.Students.objects.get(AdmissionID=student_id))

                return redirect(f"/Student/StudentShow/{student_id}")
            else:
                print("---------------",student_form.errors)
        else:
            student_form = fm.StudentForm(
                initial = { 
                    "StudentName": student_data.StudentName, 
                    "StudentPhoto": student_data.StudentPhoto,
                    "StudentDOB": student_data.StudentDOB,
                    "StudentMobileNo": student_data.StudentMobileNo,

                    "AddressLine1": student_data.AddressLine1,
                    "AddressLine2": student_data.AddressLine2,
                    "PreviousSchoolName": student_data.PreviousSchoolName,

                    "FatherName": student_data.FatherName,
                    "FatherMobileNo": student_data.FatherMobileNo,
                    "FatherWhatsappNo": student_data.FatherWhatsappNo,
                    "FatherEmail": student_data.FatherEmail,
                    "FatherQualification": student_data.FatherQualification,
                    "FatherOccupation": student_data.FatherOccupation,
                    "FatherIncome": student_data.FatherIncome,

                    "MotherName": student_data.MotherName,
                    "MotherMobileNo": student_data.MotherMobileNo,
                    "MotherWhatsappNo": student_data.FatherWhatsappNo,
                    "MotherEmail": student_data.MotherEmail,
                    "MotherQualification": student_data.MotherQualification,
                    "MotherOccupation": student_data.MotherOccupation,
                    "MotherIncome": student_data.MotherIncome,

                    
                    "GaurdianName": student_data.GaurdianName,
                    "GaurdianMobileNo": student_data.GaurdianMobileNo,
                    "GaurdianWhatsappNo": student_data.GaurdianWhatsappNo,
                    "GaurdianEmail": student_data.GaurdianEmail,
                    "GaurdianQualification": student_data.GaurdianQualification,
                    "GaurdianOccupation": student_data.GaurdianOccupation,
                    "GaurdianIncome": student_data.GaurdianIncome,
                    })

        # objset=student_data
        # jsondata=serializers.serialize("json",objset)

        context = {
            "student_form": student_form,
            "student_data": student_data,
            "gender_list":md.Gender.objects.all().order_by("GenderOrder"),
            "bloodgroup_list":md.BloodGroup.objects.all(),
            "caste_list":md.Caste.objects.all(),
            "religion_list":md.Religion.objects.all(),
            "castecategory_list":md.CasteCategory.objects.all(),
            "class_list":sm.Class.objects.filter(ClassID=student_data.Class.ClassID),
            "assignedclass_list":sm.AssignClass.objects.filter(Class=student_data.Class.ClassID,School=request.session['school_id']),
            "mothertongue_list":md.MotherTongue.objects.all(),
            "nationality_list":md.Nationality.objects.all(),
            "village_list":md.Village.objects.all(),
            "postoffice_list":md.PostOffice.objects.all(),
            "student_photo":student_data.StudentPhoto,
            "father_name":sm.Students.objects.get(AdmissionID = student_id).FatherName,
            "mother_name":sm.Students.objects.get(AdmissionID = student_id).MotherName,
            "gaurdian_name":sm.Students.objects.get(AdmissionID = student_id).GaurdianName,
            "AdmissionNo":sm.Students.objects.get(AdmissionID = student_id).AdmissionNo,
            "AdmissionDate":sm.Students.objects.get(AdmissionID = student_id).AdmissionDate,
            "data":student_data,
        }
        return render(request, "school/Pages/Update/update_student_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Admission/NewAdmission")
