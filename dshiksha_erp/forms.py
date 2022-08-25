from django import forms
import re
from . import models as md
from main.models import User
from school import models as cbm

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['Email']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['Password'] = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        if not User.objects.filter(Email = self.cleaned_data['Email']).exists():
            raise forms.ValidationError('Email does not exist')

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = md.AcademicYear
        fields = ['AcademicYear', 'OrderID', 'IsActive']

    def clean(self):
        if md.AcademicYear.objects.filter(AcademicYear = self.cleaned_data['AcademicYear']).exists():
            raise forms.ValidationError('Academic Year already exists')
        if md.AcademicYear.objects.filter(OrderID = self.cleaned_data['OrderID']).exists():
            raise forms.ValidationError("Order ID already taken")

class StateForm(forms.ModelForm):
    class Meta:
        model = md.State
        fields = ['StateName']

    def clean(self):
        if md.State.objects.filter(StateName = self.cleaned_data['StateName']).exists():
            raise forms.ValidationError('State already exists')

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['StateName']):
            raise forms.ValidationError("Enter proper State Name") 

class DistrictForm(forms.ModelForm):
    class Meta:
        model = md.District
        fields = ['DistrictName']

    def clean(self):
        if self.cleaned_data.get('State') is None:
            raise forms.ValidationError("State is required")

        if md.District.objects.filter(DistrictName = self.cleaned_data['DistrictName'], State = md.State.objects.get(StateID = self.cleaned_data.get('State').StateID)).exists():
            raise forms.ValidationError('District already exists')


        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.S]*$")
        if not namepattern.match(self.cleaned_data['DistrictName']):
            raise forms.ValidationError("Enter proper District Name") 

    def __init__(self, *args, **kwargs):
        super(DistrictForm, self).__init__(*args, **kwargs)
        self.fields['State'] = forms.ModelChoiceField(queryset=md.State.objects.all())

class TalukForm(forms.ModelForm):
    class Meta:
        model = md.Taluk
        fields = ['TalukName']

    def __init__(self, *args, **kwargs):
        super(TalukForm, self).__init__(*args, **kwargs)
        self.fields['DistrictName'] = forms.ModelChoiceField(queryset=md.District.objects.all())

    def clean(self):
        if self.cleaned_data.get('DistrictName') is None:
            raise forms.ValidationError("District is required")

        if md.Taluk.objects.filter(TalukName = self.cleaned_data['TalukName'], District = md.District.objects.get(DistrictID = self.cleaned_data['DistrictName'].DistrictID)).exists():
            raise forms.ValidationError('Taluk already exists')
        

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['TalukName']):
            raise forms.ValidationError("Enter proper Taluk Name") 

class VillageForm(forms.ModelForm):
    class Meta:
        model = md.Village
        fields = ['VillageName']
    
    def __init__(self, *args, **kwargs):
        super(VillageForm, self).__init__(*args, **kwargs)
        self.fields['TalukName'] = forms.ModelChoiceField(queryset=md.Taluk.objects.all())

    def clean(self):
        print(self.cleaned_data)
        
        if self.cleaned_data.get('TalukName') is None:
            raise forms.ValidationError("Taluk is required")
        
        if md.Village.objects.filter(VillageName = self.cleaned_data['VillageName'], Taluk = md.Taluk.objects.get(TalukID = self.cleaned_data['TalukName'].TalukID)).exists():
            raise forms.ValidationError('Village already exists')

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['VillageName']):
            raise forms.ValidationError("Enter proper Village Name")

class AreaForm(forms.ModelForm):
    class Meta:
        model = md.Area
        fields = ['AreaType']
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['AreaType']):
            raise forms.ValidationError("Enter proper Area Type")        
        
class GenderForm(forms.ModelForm):
    class Meta:
        model = md.Gender
        fields = ['GenderName', 'GenderOrder']

class NationalityForm(forms.ModelForm):
    class Meta:
        model = md.Nationality
        fields = ['NationalityName', 'CountryCode' ]
    
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['NationalityName']):
            raise forms.ValidationError("Enter proper Nationlity Name")

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['CountryCode']):
            raise forms.ValidationError("Enter proper Country Code")

class MotherTongueForm(forms.ModelForm):
    class Meta:
        model = md.MotherTongue
        fields = ['MotherTongueName']

    def clean(self):
        if md.MotherTongue.objects.filter(MotherTongueName = self.cleaned_data['MotherTongueName'].capitalize()).exists():
            raise forms.ValidationError('Mother Tongue already exists')
        
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['MotherTongueName']):
            raise forms.ValidationError("Enter proper language name")
    
class BloodGroupForm(forms.ModelForm):
    class Meta:
        model = md.BloodGroup
        fields = ['BloodGroupName']

    def clean(self):
        if md.BloodGroup.objects.filter(BloodGroupName = self.cleaned_data['BloodGroupName'].capitalize()).exists():
            raise forms.ValidationError('Blood Group already exists')

class PostOfficeForm(forms.ModelForm):
    class Meta:
        model = md.PostOffice
        fields = ['PostOfficeName', 'Pincode']
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['PostOfficeName']):
            raise forms.ValidationError("Enter proper Post Office Name")

        postpattern=re.compile("[0-9]{6}")
        if not postpattern.match(self.cleaned_data['Pincode']):
            raise forms.ValidationError("Enter proper Pincode")

        if md.PostOffice.objects.filter(Pincode = self.cleaned_data['Pincode'].capitalize()).exists():
            raise forms.ValidationError('Pincode already exists')
        
class ReligionForm(forms.ModelForm):
    class Meta:
        model = md.Religion
        fields = ['ReligionName']

    def clean(self):
        if md.Religion.objects.filter(ReligionName = self.cleaned_data['ReligionName'].capitalize()).exists():
            raise forms.ValidationError('Religion already exists')
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['ReligionName']):
            raise forms.ValidationError("Enter proper Religion Name")

class CasteCategoryForm(forms.ModelForm):
    class Meta:
        model = md.CasteCategory
        fields = ['CasteCategoryName']

    def clean(self):
        if md.CasteCategory.objects.filter(CasteCategoryName = self.cleaned_data['CasteCategoryName'].capitalize()).exists():
            raise forms.ValidationError('Caste Category already exists')

class CasteForm(forms.ModelForm):
    class Meta:
        model = md.Caste
        fields = ['CasteName']

    def __init__(self, *args, **kwargs):
        super(CasteForm, self).__init__(*args, **kwargs)
        self.fields['CasteCategory'] = forms.ModelChoiceField(queryset=md.CasteCategory.objects.all())
        self.fields['Religion'] = forms.ModelChoiceField(queryset=md.Religion.objects.all())
    
    def clean(self):
        if self.cleaned_data.get('CasteCategory') is None:
            raise forms.ValidationError("Caste Category is required")
        
        if self.cleaned_data.get('Religion') is None:
            raise forms.ValidationError("Religion is required")   
                 
        # if md.Caste.objects.filter(CasteName = self.cleaned_data['CasteName'],CasteCategory = md.CasteCategory.objects.get(CasteCategoryID = self.cleaned_data['CasteCategory'].CasteCategoryID),Religion = md.Religion.objects.get(ReligionID = self.cleaned_data['Religion'].ReligionID)).exists():
        if md.Caste.objects.filter(CasteName = self.cleaned_data['CasteName'],Religion = md.Religion.objects.get(ReligionID = self.cleaned_data['Religion'].ReligionID)).exists():
            raise forms.ValidationError('Caste already exists')

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s'.]*$")
        if not namepattern.match(self.cleaned_data['CasteName']):
            raise forms.ValidationError("Enter proper Caste Name")

class StaffSubjectForm(forms.ModelForm):
    class Meta:
        model = md.StaffSubject
        fields = ['StaffSubjectName']

    def clean(self):
        if md.StaffSubject.objects.filter(StaffSubjectName = self.cleaned_data['StaffSubjectName'].capitalize()).exists():
            raise forms.ValidationError('Staff Subject already exists')
        
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['StaffSubjectName']):
            raise forms.ValidationError("Enter proper Subject Name")

class SchoolForm(forms.ModelForm):
    class Meta:
        model = cbm.School
        fields = ['SchoolName', 'Landline','SchoolCode', 'Email', 'SchoolUsername','SyllabusType','AccountantName','AccountantEmail','AccountantMobile','CorrespondentName','CorrespondentEmail','CorrespondentMobile']#,'EstDate']#, 'SchoolDISECode','History','Website','SchoolPANNo','GSTINo']

    def __init__(self, *args, **kwaargs):
        super(SchoolForm, self).__init__(*args, **kwaargs)
        self.fields['Village'] = forms.ModelChoiceField(queryset=md.Village.objects.all())
        self.fields['Taluk'] = forms.ModelChoiceField(queryset=md.Taluk.objects.all(), required=False)
        self.fields['District'] = forms.ModelChoiceField(queryset=md.District.objects.all(), required=False)
        self.fields['State'] = forms.ModelChoiceField(queryset=md.State.objects.all(), required=False)
        self.fields['Pincode'] = forms.ModelChoiceField(queryset=md.PostOffice.objects.all())
        self.fields['PostOfficeName'] = forms.CharField(max_length=100, required=False)
        self.fields['Password'] = forms.CharField(max_length=100, widget=forms.PasswordInput)
        self.fields['ConfirmPassword'] = forms.CharField(max_length=100, widget=forms.PasswordInput)
        self.fields['CurrentAcademicYear'] = forms.ModelChoiceField(queryset= md.AcademicYear.objects.all())
        #self.fields['Insitution']=forms.ModelChoiceField(queryset=md.InstitutionLevel.objects.all())

    def clean(self):
        if self.cleaned_data['Password'] != self.cleaned_data['ConfirmPassword']:
            raise forms.ValidationError("Password do not match")

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.',]*$")
        if not namepattern.match(self.cleaned_data['SchoolName']):
            raise forms.ValidationError("Enter proper School Name")

        numpattern=re.compile("[a-zA-Z0-9]{8}")
        if not numpattern.match(self.cleaned_data['SchoolCode']):
            raise forms.ValidationError("Enter proper SchoolCode")

        sylabname=re.compile("[A-Za-z]")
        if not sylabname.match(self.cleaned_data['SyllabusType']):
            raise forms.ValidationError("Enter proper SyllabusType")

        mobilepattern=re.compile("[0-9]{10}")
        if not mobilepattern.match(self.cleaned_data['Landline']):
            raise forms.ValidationError("Enter proper school Landline No")

        if not namepattern.match(self.cleaned_data['SchoolUsername']):
            raise forms.ValidationError("Enter proper School User Name")

        if not namepattern.match(self.cleaned_data['AccountantName']):
            raise forms.ValidationError("Enter proper Accountant Name")

        if not namepattern.match(self.cleaned_data['CorrespondentName']):
            raise forms.ValidationError("Enter proper Correspondent Name")
        
        if not mobilepattern.match(self.cleaned_data['AccountantMobile']):
            raise forms.ValidationError("Enter proper Accountant MobileNo")

        if not mobilepattern.match(self.cleaned_data['CorrespondentMobile']):
            raise forms.ValidationError("Enter proper Correspondent MobileNo")

class ClassListForm(forms.ModelForm):
    class Meta:
        model = md.ClassList
        fields = ['ClassName', 'OrderID']

class ClassForm(forms.ModelForm):
    class Meta:
        model = cbm.Class
        fields = ['ClassList', 'ClassLevel']
    def clean(self):
        if self.fields['ClassList'] is None:
            raise forms.ValidationError("ClassList is required")

        if self.fields['ClassLevel'] is None:
            raise forms.ValidationError("ClassLevel is required")

    def __init__(self, *args, **kwaargs):
        super(ClassForm, self).__init__(*args, **kwaargs)
        self.fields['ClassList'] = forms.ModelChoiceField(queryset=md.ClassList.objects.all())
        self.fields['ClassLevel'] = forms.ModelChoiceField(queryset=md.ClassLevel.objects.all())



class SectionForm(forms.ModelForm):
    class Meta:
        model = md.Section
        fields = ['SectionName']

    def clean(self):
        if md.Section.objects.filter(SectionName = self.cleaned_data['SectionName'].capitalize()).exists():
            raise forms.ValidationError('Section already exists')

class DesignationForm(forms.ModelForm):
    class Meta:
        model = md.Designation
        fields = ['DesignationName']

    def clean(self):
        if md.Designation.objects.filter(DesignationName=self.cleaned_data['DesignationName'].capitalize()).exists():
            raise forms.ValidationError('Designation already exists')
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['DesignationName']):
            raise forms.ValidationError("Enter proper DesignationName")

class InstitutionLevelForm(forms.ModelForm):
    class Meta:
        model = md.InstitutionLevel
        fields = ['InstitutionLevel']
    
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['InstitutionLevel']):
            raise forms.ValidationError("Enter proper Institution Level")

class StaffQualificationForm(forms.ModelForm):
    class Meta:
        model = md.StaffQualification
        fields = ['StaffQualificationName']

    def clean(self):
        if md.StaffQualification.objects.filter(StaffQualificationName = self.cleaned_data['StaffQualificationName']).exists():
            raise forms.ValidationError('Staff Qualification already exists')

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['StaffQualificationName']):
            raise forms.ValidationError("Enter proper Qualification Name")    

class SchoolAffiliationForm(forms.ModelForm):
    class Meta:
        model = md.SchoolAffiliation
        fields = ['SchoolAffiliation']
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s]*$")
        if not namepattern.match(self.cleaned_data['SchoolAffiliation']):
            raise forms.ValidationError("Enter proper School Affiliation")

class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = md.ClassLevel
        fields = ['ClassLevelName', 'ClassLevelCode']

class FeesTypeForm(forms.ModelForm):
    class Meta:
        model = md.FeesType
        fields = ['FeesTypeName', 'FeeTypeCode']
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['FeesTypeName']):
            raise forms.ValidationError("Enter proper Fee Type Name")

class InstallmentForm(forms.ModelForm):
    class Meta:
        model = md.Installment
        fields = ['InstallmentName','OrderID']
    
    def clean(self):
        if md.Installment.objects.filter(OrderID = self.cleaned_data['OrderID']).exists():
            raise forms.ValidationError("Order ID already taken")


class SubFeeForm(forms.ModelForm):
    class Meta:
        model = md.SubFee
        fields = ['SubFeeName','FeesType']

    def __init__(self, *args, **kwaargs):
        super(SubFeeForm, self).__init__(*args, **kwaargs)
        self.fields['FeesType'] = forms.ModelChoiceField(queryset=md.FeesType.objects.all())

    def clean(self):
        if self.fields['FeesType'] is None:
            raise forms.ValidationError("Fees Type is required")
        
        if md.SubFee.objects.filter(SubFeeName=self.cleaned_data['SubFeeName'], FeesType = md.FeesType.objects.get(FeesTypeID = self.cleaned_data['FeesType'].FeesTypeID)).exists():
            raise forms.ValidationError('Sub Fee Type Already Exist')
        
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s .]*$")
        if not namepattern.match(self.cleaned_data['SubFeeName']):
            raise forms.ValidationError("Enter proper subfee name")

class ClassLevelFeesForm(forms.ModelForm):
    class Meta:
        model = md.ClassLevelFees
        fields = ['ClassLevel', 'FeesType']

    def __init__(self, *args, **kwaargs):
        super(ClassLevelFeesForm, self).__init__(*args, **kwaargs)
        self.fields['ClassLevel'] = forms.ModelChoiceField(queryset=md.ClassLevel.objects.all())
        self.fields['FeesType'] = forms.ModelChoiceField(queryset=md.FeesType.objects.all())

class BankForm(forms.ModelForm):
    class Meta:
        model = md.Bank
        fields = ['BankName','OrderID']

    def clean(self):
        if md.Bank.objects.filter(BankName = self.cleaned_data['BankName']).exists():
            raise forms.ValidationError('Bank already exists')
        
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['BankName']):
            raise forms.ValidationError("Enter proper Bank name")

class OnlineForm(forms.ModelForm):
    class Meta:
        model = md.Online
        fields = ['OnlineAppName','OrderID']

    def clean(self):
        if md.Online.objects.filter(OnlineAppName = self.cleaned_data['OnlineAppName']).exists():
            raise forms.ValidationError('State already exists')

        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['OnlineAppName']):
            raise forms.ValidationError("Enter proper OnlineApp name")
