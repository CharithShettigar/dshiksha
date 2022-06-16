from django.db import models
import uuid
from main.models import User


# Create your models here.

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


class StaffProQualification(models.Model):
    StaffProQualificationID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    StaffProQualificationName = models.CharField(max_length=50)


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

class MediumOfInstruction(models.Model):
    MediumOfInstructionID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    MediumOfInstruction = models.CharField(max_length=50)

class InstitutionLevel(models.Model):
    InstitutionLevelID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    InstitutionLevel = models.CharField(max_length=100)


class SyllabusType(models.Model):
    SyllabusTypeID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    SyllabusType = models.CharField(max_length=100)


class ModeOfPayment(models.Model):
    ModeOfPaymentID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ModeOfPayment = models.CharField(max_length=50)
    OrderID = models.IntegerField()


class PaymentStatus(models.Model):
    PaymentStatusID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    PaymentStatus = models.CharField(max_length=50)


class Correspondent(models.Model):
    CorrespondentID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CorrespondentFirstName = models.CharField(max_length=100)
    CorrespondentLastName = models.CharField(max_length=100, null=True)
    CorrespondentEmail = models.EmailField(max_length=100)
    CorrespondentMobile = models.CharField(max_length=100)
    CorrespondentWhatsAppNo = models.CharField(max_length=100)


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