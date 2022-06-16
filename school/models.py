from django.db import models
import uuid
from dshiksha_erp import models as erp
from main.models import User


# Create your models here.
class Class(models.Model):
    ClassID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ClassList = models.ForeignKey(erp.ClassList, on_delete=models.CASCADE)
    ClassLevel = models.ForeignKey(erp.ClassLevel, on_delete=models.CASCADE)


class Accountant(models.Model):
    AccountantID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    AccountantName = models.CharField(max_length=100)
    AccountantEmail = models.EmailField(max_length=100)
    AccountantMobile = models.CharField(max_length=100)
    AccountantWhatsAppNo = models.CharField(max_length=100)


class School(models.Model):
    SchoolID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    SchoolName = models.CharField(max_length=100)
    SchoolLogo = models.CharField(max_length=250)
    Pincode = models.ForeignKey(erp.PostOffice, on_delete=models.CASCADE)
    SchoolDISECode = models.CharField(max_length=100)
    SchoolType = models.CharField(max_length=100)
    Correspondent = models.ForeignKey(erp.Correspondent, on_delete=models.CASCADE, null=True)
    Area = models.ForeignKey(erp.Area, on_delete=models.CASCADE, null=True)
    Syllabus = models.ForeignKey(erp.SyllabusType, on_delete=models.CASCADE, null=True)
    erp.InsitutionLevel = models.ForeignKey(erp.InstitutionLevel, on_delete=models.CASCADE, null=True)
    Landline = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Website = models.CharField(max_length=100)
    Accountant = models.ForeignKey(Accountant, on_delete=models.CASCADE, null=True)
    EstDate = models.DateField(null=True)
    History = models.TextField(max_length=5000)
    SchoolPANNo = models.CharField(max_length=100)
    GSTINo = models.CharField(max_length=100)
    Village = models.ForeignKey(erp.Village, on_delete=models.CASCADE)
    SchoolCode = models.CharField(max_length=25)
    SchoolUsername = models.CharField(max_length=50)
    Parish = models.ForeignKey(erp.Parish, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CurrentAcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE)


class Staff(models.Model):
    StaffID = models.UUIDField(primary_key=True, default = uuid.uuid4)
    SchoolID = models.ForeignKey(School, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    StaffName = models.CharField(max_length=100)
    StaffEmailID = models.EmailField(max_length=100)
    StaffMobile = models.CharField(max_length=10)
    StaffPhoto = models.CharField(max_length=250)
    Gender = models.ForeignKey(erp.Gender, on_delete=models.CASCADE, null=True)
    DOB = models.DateField(null=True)
    BloodGroup = models.ForeignKey(erp.BloodGroup, on_delete=models.CASCADE, null=True)
    MaritalStatus = models.ForeignKey(erp.MaritalStatus, on_delete = models.CASCADE, null=True)
    Caste = models.ForeignKey(erp.Caste, on_delete = models.CASCADE, null=True)
    MotherTongue = models.ForeignKey(erp.MotherTongue, on_delete = models.CASCADE, null=True)
    AddressLine1 = models.CharField(max_length=100)
    AddressLine2 = models.CharField(max_length=100)
    Village = models.ForeignKey(erp.Village, on_delete = models.CASCADE, null=True)
    Pincode = models.ForeignKey(erp.PostOffice, on_delete = models.CASCADE, null=True)
    StaffWhatsAppNo = models.CharField(max_length=25)
    # StaffWorkPost = models.CharField(max_length=100)
    Designation = models.ForeignKey(erp.Designation, on_delete = models.CASCADE, null=True)
    StaffQualification = models.ForeignKey(erp.StaffQualification, on_delete = models.CASCADE, null=True)
    StaffProQualification = models.ForeignKey(erp.StaffProQualification, on_delete = models.CASCADE, null=True)
    Subject1 = models.ForeignKey(erp.StaffSubject, on_delete = models.CASCADE, related_name='Subject1', null=True)
    Subject2 = models.ForeignKey(erp.StaffSubject, on_delete = models.CASCADE, related_name='Subject2', null=True)
    NatureOfAppointment = models.ForeignKey(erp.NatureOfAppointment, on_delete = models.CASCADE, null=True)
    DateOfAppointment = models.DateField(null=True)
    DateOfRetirement = models.DateField(null=True)
    ProvidentFund = models.BooleanField(default=False)
    ESI = models.BooleanField(default=False)
    ProfessionalTax = models.BooleanField(default=False)
    Gratuity = models.BooleanField(default=False)
    CautionDeposit = models.BooleanField(default=False)
    StaffNo = models.CharField(max_length=50)
    AcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE)


class CBSEHead(models.Model):
    CBSEHeadID = models.UUIDField(default=uuid.uuid4, primary_key=True)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    Staff = models.ForeignKey(Staff, on_delete=models.CASCADE)


class AssignClass(models.Model):
    AssignClassID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Section = models.ForeignKey(erp.Section, on_delete=models.CASCADE)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    AcademicYear = models.ForeignKey(erp.AcademicYear, on_delete=models.CASCADE)


class Subject(models.Model):
    SubjectID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    SubjectName = models.CharField(max_length=50)
    AssignClass = models.ForeignKey(AssignClass, on_delete=models.CASCADE)


class Chapter(models.Model):
    ChapterID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ChapterName = models.CharField(max_length=50)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class StaffNo(models.Model):
    StaffNoID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    StaffNo = models.CharField(max_length=50)


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
    FatherName = models.CharField(max_length=100)
    FatherMobileNo = models.CharField(max_length=30)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    School = models.ForeignKey(School, on_delete=models.CASCADE)
    ApplicationDate = models.DateField()
    Amount = models.FloatField()
    ModeOfPayment = models.ForeignKey(erp.ModeOfPayment, on_delete=models.CASCADE)
    PaymentStatus = models.ForeignKey(erp.PaymentStatus, on_delete=models.CASCADE)

class Admission(models.Model):
    AdmissionID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    SchoolID = models.ForeignKey(School, on_delete=models.CASCADE)
    ApplicatioNo = models.CharField(max_length=50) 
    StudentName = models.CharField(max_length=100)
    FatherName = models.CharField(max_length=100)
    Amount = models.FloatField()
    ApplicationDate = models.DateField()
    Class = models.CharField(max_length=100)

class Students(models.Model):
    pass