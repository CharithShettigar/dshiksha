from gc import collect
from pyexpat import model
from re import T
from tkinter import CASCADE
from datetime import datetime
import os
from django.db import models
import uuid
from dshiksha_erp import models as erp
from main.models import User

#upload file to static/uploads
def filepath_school(request,filename):
    old_file=filename
    timenow=datetime.now().strftime("%Y%m%d%H%M%S")
    # filename=f'{School.SchoolName}_{timenow}_{old_file}'
    filename=f'{timenow}_{old_file}'
    return os.path.join('uploads/school',filename)

def filepath_staff(request,filename):
    old_file=filename
    timenow=datetime.now().strftime("%Y%m%d%H%M%S")
    filename=f'{timenow}_{old_file}'
    # filename=f'{Staff.StaffName}_{timenow}_{old_file}'
    return os.path.join('uploads/staff',filename)
    
def filepath_student(request,filename):
    old_file=filename
    timenow=datetime.now().strftime("%Y%m%d%H%M%S")
    filename=f'{timenow}_{old_file}'
    # filename=f'{Students.StudentName}_{timenow}_{old_file}'
    return os.path.join('uploads/student',filename)

# Create your models here.
class Class(models.Model):
    ClassID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ClassList = models.ForeignKey(erp.ClassList, on_delete=models.CASCADE)
    ClassLevel = models.ForeignKey(erp.ClassLevel, on_delete=models.CASCADE)


class School(models.Model):
    SchoolID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    SchoolName = models.CharField(max_length=100)
    SchoolLogo = models.ImageField(upload_to=filepath_school,null=True)
    SchoolSeal = models.ImageField(upload_to=filepath_school,null=True)
    SchoolSign = models.ImageField(upload_to=filepath_school,null=True)
    Pincode = models.ForeignKey(erp.PostOffice, on_delete=models.CASCADE)
    SchoolDISECode = models.CharField(max_length=100)
    SchoolType = models.CharField(max_length=100)
    Area = models.ForeignKey(erp.Area, on_delete=models.CASCADE, null=True)
    InsitutionLevel = models.ForeignKey(erp.InstitutionLevel, on_delete=models.CASCADE, null=True)
    Landline = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Website = models.CharField(max_length=100)
    EstDate = models.DateField(null=True)
    History = models.TextField(max_length=5000)
    SchoolPANNo = models.CharField(max_length=100)
    GSTINo = models.CharField(max_length=100)
    Village = models.ForeignKey(erp.Village, on_delete=models.CASCADE)
    SchoolCode = models.CharField(max_length=25)
    SchoolUsername = models.CharField(max_length=50)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CurrentAcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE)
    SyllabusType = models.CharField(max_length=100)

    AccountantName = models.CharField(max_length=100)
    AccountantEmail = models.EmailField(max_length=100)
    AccountantMobile = models.CharField(max_length=100)
    AccountantWhatsAppNo = models.CharField(max_length=100)

    CorrespondentFirstName = models.CharField(max_length=100)
    CorrespondentLastName = models.CharField(max_length=100, null=True)
    CorrespondentEmail = models.EmailField(max_length=100)
    CorrespondentMobile = models.CharField(max_length=100)
    CorrespondentWhatsAppNo = models.CharField(max_length=100)


class Staff(models.Model):
    StaffID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    SchoolID = models.ForeignKey(School, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    StaffName = models.CharField(max_length=100)
    StaffEmailID = models.EmailField(max_length=100)
    StaffMobile = models.CharField(max_length=10)
    StaffPhoto = models.ImageField(upload_to=filepath_staff,null=True)
    Gender = models.ForeignKey(erp.Gender, on_delete=models.CASCADE, null=True)
    DOB = models.DateField(null=True)
    BloodGroup = models.ForeignKey(erp.BloodGroup, on_delete=models.CASCADE, null=True)
    MaritalStatus = models.ForeignKey(erp.MaritalStatus, on_delete=models.CASCADE, null=True)
    Caste = models.ForeignKey(erp.Caste, on_delete=models.CASCADE, null=True)
    MotherTongue = models.ForeignKey(erp.MotherTongue, on_delete=models.CASCADE, null=True)
    AddressLine1 = models.CharField(max_length=100)
    AddressLine2 = models.CharField(max_length=100)
    Village = models.ForeignKey(erp.Village, on_delete=models.CASCADE, null=True)
    Pincode = models.ForeignKey(erp.PostOffice, on_delete=models.CASCADE, null=True)
    StaffWhatsAppNo = models.CharField(max_length=25)
    # StaffWorkPost = models.CharField(max_length=100)
    Designation = models.ForeignKey(erp.Designation, on_delete=models.CASCADE, null=True)
    StaffQualification = models.ForeignKey(erp.StaffQualification, on_delete=models.CASCADE, null=True)
    Subject1 = models.ForeignKey(erp.StaffSubject, on_delete=models.CASCADE, related_name='Subject1', null=True)
    Subject2 = models.ForeignKey(erp.StaffSubject, on_delete=models.CASCADE, related_name='Subject2', null=True)
    Designation = models.ForeignKey(erp.Designation, on_delete = models.CASCADE, null=True)
    StaffQualification = models.ForeignKey(erp.StaffQualification, on_delete = models.CASCADE, null=True)
    Subject1 = models.ForeignKey(erp.StaffSubject, on_delete = models.CASCADE, related_name='Subject1', null=True)
    Subject2 = models.ForeignKey(erp.StaffSubject, on_delete = models.CASCADE, related_name='Subject2', null=True)
    DateOfAppointment = models.DateField(null=True)
    DateOfRetirement = models.DateField(null=True)
    StaffNo = models.CharField(max_length=50)
    AcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE, null=True)


class SCHOOLHead(models.Model):
    SCHOOLHeadID = models.UUIDField(default=uuid.uuid4, primary_key=True)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Staff = models.ForeignKey(Staff, on_delete=models.CASCADE)


class AssignClass(models.Model):
    AssignClassID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Section = models.ForeignKey(erp.Section, on_delete=models.CASCADE)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    AcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE)


class Subject(models.Model):
    SubjectID = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    SubjectName = models.CharField(max_length=50)
    AssignClass = models.ForeignKey(AssignClass, on_delete=models.CASCADE)


class Chapter(models.Model):
    ChapterID = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    ChapterName = models.CharField(max_length=50)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class ApplicationNo(models.Model):
    ApplicationNoID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Amount = models.FloatField()
    AcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE)
    ApplicationNo = models.IntegerField()


class Application(models.Model):
    ApplicationID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ApplicationNo = models.CharField(max_length=100)
    StudentName = models.CharField(max_length=100)
    StudentDOB = models.DateField()
    Gender = models.ForeignKey(erp.Gender, on_delete=models.CASCADE, null=True)
    StudentMobileNo = models.CharField(max_length=30)
    ParentName = models.CharField(max_length=100)
    ParentMobileNo = models.CharField(max_length=30)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    SchoolID = models.ForeignKey(School, on_delete=models.CASCADE)
    ApplicationDate = models.DateField()
    Amount = models.FloatField()
    ModeOfPayment = models.ForeignKey(erp.ModeOfPayment, on_delete=models.CASCADE)
    #PaymentStatus = models.ForeignKey(erp.PaymentStatus, on_delete=models.CASCADE)


class Students(models.Model):
    AdmissionID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    AdmissionNo = models.CharField(max_length=100)
    AdmissionDate = models.DateField()
    PreviousSchoolName = models.CharField(max_length=100,null=True)
    SchoolID = models.ForeignKey(School, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    AssignedClass = models.ForeignKey(AssignClass, on_delete=models.CASCADE,null=True)
    Application = models.ForeignKey(Application, on_delete=models.CASCADE,null=True)

    # student info
    StudentName = models.CharField(max_length=100)
    StudentDOB = models.DateField()
    Gender = models.ForeignKey(erp.Gender, on_delete=models.CASCADE, null=True)
    StudentMobileNo = models.CharField(max_length=30)
    StudentPhoto = models.CharField(max_length=100)
    Village = models.ForeignKey(erp.Village, on_delete=models.CASCADE, null=True)
    Nationality = models.ForeignKey(erp.Nationality, on_delete=models.CASCADE, null=True)
    BloodGroup = models.ForeignKey(erp.BloodGroup, on_delete=models.CASCADE, null=True)
    Religion = models.ForeignKey(erp.Religion, on_delete=models.CASCADE, null=True)
    CasteCategory = models.ForeignKey(erp.CasteCategory, on_delete=models.CASCADE, null=True)
    Caste = models.ForeignKey(erp.Caste, on_delete=models.CASCADE, null=True)
    MotherTongue = models.ForeignKey(erp.MotherTongue, on_delete=models.CASCADE, null=True)
    AssignedClass = models.ForeignKey(AssignClass, on_delete=models.CASCADE,null=True)
    StudentPhoto = models.ImageField(upload_to=filepath_student,null=True)
    
    Village = models.ForeignKey(erp.Village, on_delete = models.CASCADE, null=True)
    Nationality=models.ForeignKey(erp.Nationality,on_delete=models.CASCADE,null=True)
    BloodGroup = models.ForeignKey(erp.BloodGroup,on_delete=models.CASCADE, null=True)
    Religion = models.ForeignKey(erp.Religion, on_delete=models.CASCADE,null=True)
    CasteCategory = models.ForeignKey(erp.CasteCategory, on_delete=models.CASCADE,null=True)
    Caste = models.ForeignKey(erp.Caste, on_delete=models.CASCADE,null=True)
    MotherTongue = models.ForeignKey(erp.MotherTongue, on_delete = models.CASCADE, null=True)

    # Address info
    AddressLine1 = models.CharField(max_length=100)
    AddressLine2 = models.CharField(max_length=100)
    Village = models.ForeignKey(erp.Village, on_delete=models.CASCADE, null=True)
    Pincode = models.ForeignKey(erp.PostOffice, on_delete=models.CASCADE, null=True)

    # father info
    FatherName = models.CharField(max_length=100,null=True)
    FatherMobileNo = models.CharField(max_length=100,null=True)
    FatherWhatsappNo = models.CharField(max_length=100,null=True)
    FatherEmail = models.EmailField(max_length=100,null=True)
    FatherQualification = models.CharField(max_length=100,null=True)
    FatherOccupation = models.CharField(max_length=100,null=True)
    FatherIncome = models.FloatField(null=True)

    # Mother info
    MotherName = models.CharField(max_length=100,null=True)
    MotherMobileNo = models.CharField(max_length=100,null=True)
    MotherWhatsappNo = models.CharField(max_length=100,null=True)
    MotherEmail = models.EmailField(max_length=100,null=True)
    MotherQualification = models.CharField(max_length=100,null=True)
    MotherOccupation = models.CharField(max_length=100,null=True)
    MotherIncome = models.FloatField(null=True)

    # Guardian info
    GaurdianName = models.CharField(max_length=100,null=True)
    GaurdianMobileNo = models.CharField(max_length=100,null=True)
    GaurdianWhatsappNo = models.CharField(max_length=100,null=True)
    GaurdianEmail = models.EmailField(max_length=100,null=True)
    GaurdianQualification = models.CharField(max_length=100,null=True)
    GaurdianOccupation = models.CharField(max_length=100,null=True)
    GaurdianIncome = models.FloatField(null=True)

# Attendance table

class Attendance(models.Model):
    AttendanceID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    StudentID=models.ForeignKey(Students, on_delete=models.CASCADE)
    AssignClass = models.ForeignKey(AssignClass, on_delete=models.CASCADE,null=True)
    AttendanceDate=models.DateField()
    AttendanceMark=models.CharField(max_length=100)
    SchoolID = models.ForeignKey(School, on_delete=models.CASCADE)

class AssignFeeAmount(models.Model):
    AssignFeeAmountID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Class  = models.ForeignKey(Class,on_delete=models.CASCADE)
    FeesType = models.ForeignKey(erp.FeesType, on_delete=models.CASCADE)
    SubFee = models.ForeignKey(erp.SubFee, on_delete=models.CASCADE)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Amount = models.FloatField()
    AcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE)

class CollectFee(models.Model):
    CollectFeeID=models.UUIDField(primary_key=True, default=uuid.uuid4)
    Admission = models.ForeignKey(Students, on_delete=models.CASCADE)
    AssignClass = models.ForeignKey(AssignClass, on_delete=models.CASCADE,null=True)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    ModeOfPayment = models.ForeignKey(erp.ModeOfPayment,on_delete=models.CASCADE,null=True)
    RefferenceNO = models.CharField(max_length=100, null=True)
    Bank = models.ForeignKey(erp.Bank, on_delete=models.CASCADE, null=True)
    Online = models.ForeignKey(erp.Online, on_delete=models.CASCADE, null=True)
    PaidAmount = models.FloatField()
    Installment = models.ForeignKey(erp.Installment, on_delete=models.CASCADE,null=True)
    PaymentStatus = models.CharField(max_length=100,null=True)
    CollectFeeDate = models.DateField(null=True)
    CollectFeeNo = models.CharField(max_length=100)

class Feedback(models.Model):
    FeedbackID=models.UUIDField(primary_key=True, default=uuid.uuid4)
    Feedback=models.CharField(max_length=500)
    School=models.ForeignKey(School, on_delete=models.CASCADE)
    File=models.FileField(upload_to=filepath_school,null=True)