from django.db import models
import uuid
from main.models import User


# Create your models here.
class AcademicYear(models.Model):
    AcademicYearID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AcademicYear = models.CharField(max_length=50)
    IsActive = models.BooleanField()
    OrderID = models.IntegerField(unique=True)


class State(models.Model):
    StateID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    StateName = models.CharField(max_length=50)


class District(models.Model):
    DistrictID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    DistrictName = models.CharField(max_length=50)
    State = models.ForeignKey(State, on_delete=models.CASCADE)


class Taluk(models.Model):
    TalukID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    TalukName = models.CharField(max_length=50)
    District = models.ForeignKey(District, on_delete=models.CASCADE)


class Village(models.Model):
    VillageID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    VillageName = models.CharField(max_length=50)
    Taluk = models.ForeignKey(Taluk, on_delete=models.CASCADE)

class Area(models.Model):
    AreaID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    AreaType = models.CharField(max_length=100)

class Gender(models.Model):
    GenderID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    GenderName = models.CharField(max_length=50)
    GenderOrder = models.IntegerField(unique=True)


class Nationality(models.Model):
    NationalityID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    NationalityName = models.CharField(max_length=50)
    CountryCode = models.CharField(max_length=50)


class MotherTongue(models.Model):
    MotherTongueID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    MotherTongueName = models.CharField(max_length=50)


class BloodGroup(models.Model):
    BloodGroupID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    BloodGroupName = models.CharField(max_length=50)


class StaffQualification(models.Model):
    StaffQualificationID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    StaffQualificationName = models.CharField(max_length=50)

class Religion(models.Model):
    ReligionID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ReligionName = models.CharField(max_length=50)

class CasteCategory(models.Model):
    CasteCategoryID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    CasteCategoryName = models.CharField(max_length=50)


class Caste(models.Model):
    CasteID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    CasteName = models.CharField(max_length=50)
    CasteCategory = models.ForeignKey(CasteCategory, on_delete=models.CASCADE)
    Religion = models.ForeignKey(Religion, on_delete=models.CASCADE)


class MaritalStatus(models.Model):
    MaritalStatusID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    MaritalStatus = models.CharField(max_length=50)


class Designation(models.Model):
    DesignationID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    DesignationName = models.CharField(max_length=50)


class PostOffice(models.Model):
    PostOfficeID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    PostOfficeName = models.CharField(max_length=50)
    Pincode = models.CharField(max_length=50)


class ClassLevel(models.Model):
    ClassLevelID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ClassLevelName = models.CharField(max_length=50)
    ClassLevelCode = models.CharField(max_length=50)


class ClassList(models.Model):
    ClassID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ClassName = models.CharField(max_length=50)
    OrderID = models.IntegerField()


class Section(models.Model):
    SectionID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    SectionName = models.CharField(max_length=50)


class StaffSubject(models.Model):
    StaffSubjectID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    StaffSubjectName = models.CharField(max_length=50)


class SchoolAffiliation(models.Model):
    SchoolAffiliationID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    SchoolAffiliation = models.CharField(max_length=50)


class ModeOfTransport(models.Model):
    ModeOfTransportID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    TransportName = models.CharField(max_length=50)
    OrderID = models.IntegerField()


class TransportData(models.Model):
    TransportDataID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ModeOfTransport = models.ForeignKey(ModeOfTransport, on_delete=models.CASCADE)
    DriverName = models.CharField(max_length=50, null=True)
    DriverMobileNo = models.CharField(max_length=50, null=True)
    DriverEmail = models.EmailField(max_length=50, null=True)
    DriverAddress = models.TextField(null=True)


class NatureOfAppointment(models.Model):
    NatureOfAppointmentID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    NatureOfAppointment = models.CharField(max_length=100)


class SchoolType(models.Model):
    SchoolTypeID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    SchoolType = models.CharField(max_length=100)


class InstitutionLevel(models.Model):
    InstitutionLevelID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    InstitutionLevel = models.CharField(max_length=100)

class ModeOfPayment(models.Model):
    ModeOfPaymentID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ModeOfPayment = models.CharField(max_length=50)
    OrderID = models.IntegerField()


class PaymentStatus(models.Model):
    PaymentStatusID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    PaymentStatus = models.CharField(max_length=50)

class FeesType(models.Model):
    FeesTypeID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    FeesTypeName = models.CharField(max_length=50)
    FeeTypeCode = models.CharField(max_length=50)


class Installment(models.Model):
    InstallmentID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    InstallmentName = models.CharField(max_length=50)


class SubFee(models.Model):
    SubFeeID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    FeesType = models.ForeignKey(FeesType, on_delete=models.CASCADE)
    SubFeeName = models.CharField(max_length=50)

class ClassLevelFees(models.Model):
    ClassLevelFeesID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ClassLevel = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    FeesType = models.ForeignKey(FeesType, on_delete=models.CASCADE)

class Bank(models.Model):
    BankID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    BankName = models.CharField(max_length=50)
    OrderID = models.IntegerField()

class Online(models.Model):
    OnlineID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    OnlineAppName = models.CharField(max_length=50)
    OrderID = models.IntegerField()