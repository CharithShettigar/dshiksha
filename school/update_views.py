from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from school import forms as fm
from dshiksha_erp import models as md
from school import models as sm
from main.models import UserTypes, User
import dshiksha_erp.models as erp

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
                school_data.SchoolLogo=school_form.cleaned_data['SchoolLogo']
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
                school_data.CorrespondentFirstName=school_form.cleaned_data['CorrespondentFirstName']
                school_data.CorrespondentLastName=school_form.cleaned_data['CorrespondentLastName']
                school_data.CorrespondentEmail=school_form.cleaned_data['CorrespondentEmail']
                school_data.CorrespondentMobile=school_form.cleaned_data['CorrespondentMobile']
                school_data.CorrespondentWhatsAppNo=school_form.cleaned_data['CorrespondentWhatsAppNo']
                school_data.save()
                return redirect("/School/SchoolInfo")
            else:
                print("---------------",school_form.errors)
        else:
            school_form = fm.SchoolForm(
                initial = { 
                    "SchoolName": school_data.SchoolName, 
                    # "SchoolCode": school_data.SchoolCode,
                    "SchoolLogo" : school_data.SchoolLogo,
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

                    "CorrespondentFirstName": school_data.CorrespondentFirstName,
                    "CorrespondentLastName": school_data.CorrespondentLastName,
                    "CorrespondentEmail": school_data.CorrespondentEmail,
                    "CorrespondentMobile": school_data.CorrespondentMobile,
                    "CorrespondentWhatsAppNo": school_data.CorrespondentWhatsAppNo,
                    })

        context = {
            "school_data": school_data,
            "school_form": school_form,
            "village_list":md.Village.objects.all(),
            "currentacademicYear_list":md.AcademicYear.objects.all(),
            "post_list":md.PostOffice.objects.all(),
            "area_list":md.Area.objects.all(),
            "institution_list":md.InstitutionLevel.objects.all(),
            "school_id": request.session['school_id'],
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
                staff_data.StaffPhoto=staff_form.cleaned_data['StaffPhoto']
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
                return redirect(f"/Staff/StaffInfoShow/{staff_id}")
            else:
                print("-----------",staff_form.cleaned_data['StaffName'])
                print("---------------",staff_form.errors)
        else:
            staff_form = fm.StaffForm(
                initial = { 
                    "StaffName": staff_data.StaffName, 
                    "StaffEmailID" : staff_data.StaffEmailID,
                    "StaffMobile": staff_data.StaffMobile,
                    "StaffPhoto": staff_data.StaffPhoto,
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
        }
        return render(request, "school/Pages/Update/update_staff_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/StaffInfo")


def update_student(request, student_id):
    if request.user.is_authenticated:
        student_data = sm.Students.objects.get(AdmissionID = student_id)

        if request.method == "POST":
            student_form = fm.StaffForm(request.POST)
            if student_form.is_valid():
                student_data.StaffName=student_form.cleaned_data['StaffName']
                student_data.StaffEmailID= student_form.cleaned_data['StaffEmailID']
                student_data.StaffMobile= student_form.cleaned_data['StaffMobile']
                student_data.StaffPhoto=student_form.cleaned_data['StaffPhoto']
                student_data.Gender= student_form.cleaned_data['Gender']
                student_data.DOB= student_form.cleaned_data['DOB']
                student_data.BloodGroup= student_form.cleaned_data['BloodGroup']
                student_data.MaritalStatus= student_form.cleaned_data['MaritalStatus']
                student_data.Caste= student_form.cleaned_data['Caste']
                student_data.MotherTongue= student_form.cleaned_data['MotherTongue']
                student_data.AddressLine1= student_form.cleaned_data['AddressLine1']
                student_data.AddressLine2= student_form.cleaned_data['AddressLine2']
                student_data.Village= student_form.cleaned_data['Village']
                student_data.Pincode= student_form.cleaned_data['Pincode']
                student_data.StaffWhatsAppNo= student_form.cleaned_data['StaffWhatsAppNo']
                student_data.Designation= student_form.cleaned_data['Designation']
                student_data.StaffQualification= student_form.cleaned_data['StaffQualification']
                student_data.Subject1= student_form.cleaned_data['Subject1']
                student_data.Subject2= student_form.cleaned_data['Subject2']
                student_data.DateOfAppointment=student_form.cleaned_data['DateOfAppointment']
                student_data.DateOfRetirement= student_form.cleaned_data['DateOfRetirement']
                student_data.AcademicYear= student_form.cleaned_data['AcademicYear']
                student_data.save()
                return redirect(f"/Staff/StaffInfoShow/{student_id}")
            else:
                print("-----------",student_form.cleaned_data['StaffName'])
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
                    "FatherMobileNo": student_data.MotherMobileNo,
                    "MotherWhatsappNo": student_data.FatherWhatsappNo,
                    "MotherEmail": student_data.MotherEmail,
                    "MotherQualification": student_data.MotherQualification,
                    "MotherOccupation": student_data.MotherOccupation,
                    "MotherIncome": student_data.MotherIncome,

                    
                    "GaurdianName": student_data.GaurdianName,
                    "GaurdianMobileNo": student_data.GaurdianMobileNo,
                    "FatherWhatsappNo": student_data.GaurdianWhatsappNo,
                    "GaurdianEmail": student_data.GaurdianEmail,
                    "GaurdianQualification": student_data.GaurdianQualification,
                    "GaurdianOccupation": student_data.GaurdianOccupation,
                    "GaurdianIncome": student_data.GaurdianIncome,
                    })

        context = {
            "student_form": student_form,
            "student_data": student_data,
            "gender_list":md.Gender.objects.all(),
            "bloodgroup_list":md.BloodGroup.objects.all(),
            "caste_list":md.Caste.objects.all(),
            "religion_list":md.Religion.objects.all(),
            "castecategory_list":md.CasteCategory.objects.all(),
            "class_list":sm.Class.objects.all(),
            "mothertongue_list":md.MotherTongue.objects.all(),
            "nationality_list":md.Nationality.objects.all(),
            "village_list":md.Village.objects.all(),
            "postoffice_list":md.PostOffice.objects.all(),
        }
        return render(request, "school/Pages/Update/update_student_info.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Admission/NewAdmission")
