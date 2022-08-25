import re
from django import forms
from main.models import User
from school import models as sm
from dshiksha_erp import models as md

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['Email']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['Password'] = forms.CharField(widget=forms.PasswordInput)

    def clean(self) :
        pass

class StaffCreateForm(forms.ModelForm):
    class Meta:
        model = sm.Staff    
        fields = ['StaffName', 'StaffEmailID', 'StaffMobile','Designation','StaffQualification','Gender']
        # exclude = ['UserID']
        # fields = ['StaffName', 'StaffEmailID', 'StaffMobile','DOB','Gender','BloodGroup','MaritalStatus','Caste','MotherTongue','AddressLine1','AddressLine2']

    def __init__(self, *args, **kwaargs):
        super(StaffCreateForm, self).__init__(*args, **kwaargs)
        self.fields['Password'] = forms.CharField(widget=forms.PasswordInput)
        self.fields['PasswordConfirm'] = forms.CharField(widget=forms.PasswordInput)
            
    def clean(self):
        if self.cleaned_data['Password'] != self.cleaned_data['PasswordConfirm']:
            raise forms.ValidationError("Password does not match")
        
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['StaffName']):
            raise forms.ValidationError("Enter proper name")

        mobilepattern=re.compile("[0-9]{10}")
        if not mobilepattern.match(self.cleaned_data['StaffMobile']):
            raise forms.ValidationError("Enter proper mobile number")


class StaffForm(forms.ModelForm):
    class Meta:
        model = sm.Staff    
        exclude = ['UserID','SchoolID','StaffNo','StaffID','StaffPhoto']

    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['StaffName']):
            raise forms.ValidationError("Enter proper name")

        mobilepattern=re.compile("[0-9]{10}")
        if not mobilepattern.match(self.cleaned_data['StaffMobile']):
            raise forms.ValidationError("Enter proper mobile number")

        if not mobilepattern.match(self.cleaned_data['StaffWhatsAppNo']):
            raise forms.ValidationError("Enter proper whatsapp number")


class ApplicationFeesForm(forms.ModelForm):
    class Meta:
        model = sm.ApplicationNo
        fields = ['Amount']

    def __init__(self, *args, **kwaargs):
        super(ApplicationFeesForm, self).__init__(*args, **kwaargs)
        self.fields['Amount'] = forms.FloatField()
        self.fields['ApplicationNoID'] = forms.ModelChoiceField(queryset=sm.ApplicationNo.objects.all())
    
    def clean(self):
        if self.cleaned_data['Amount']<0:
            raise forms.ValidationError("Amount should be greater than Zero")



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = sm.Application
        fields = ['StudentName','Gender','StudentDOB','StudentMobileNo','ParentName', 'ParentMobileNo','Class','Amount','ModeOfPayment']

    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['StudentName']):
            raise forms.ValidationError("Enter proper Student name")

        if not namepattern.match(self.cleaned_data['ParentName']):
            raise forms.ValidationError("Enter proper Parent name")

        mobilepattern=re.compile("[0-9]{10}")
        if not mobilepattern.match(self.cleaned_data['StudentMobileNo']):
            raise forms.ValidationError("Enter proper Student mobile number")

        if not mobilepattern.match(self.cleaned_data['ParentMobileNo']):
            raise forms.ValidationError("Enter proper Parent mobile number")


class SchoolForm(forms.ModelForm):
    class Meta:
        model = sm.School
        exclude = ['UserID','SchoolID','SchoolType','SchoolUsername','SchoolCode','Email','SchoolLogo','SchoolSeal','SchoolSign']
    
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.,]*$")
        if not namepattern.match(self.cleaned_data['SchoolName']):
            raise forms.ValidationError("Enter proper School name")

        numpattern=re.compile("[0-9]{11}")
        if not numpattern.match(self.cleaned_data['SchoolDISECode']):
            raise forms.ValidationError("Enter proper SchoolDISECode")

        if not namepattern.match(self.cleaned_data['SyllabusType']):
            raise forms.ValidationError("Enter proper SyllabusType")

        mobilepattern=re.compile("[0-9]{10}")
        if not mobilepattern.match(self.cleaned_data['Mobile']):
            raise forms.ValidationError("Enter proper school MobileNo")

        if not mobilepattern.match(self.cleaned_data['Landline']):
            raise forms.ValidationError("Enter proper school LandlineNo")

        if not namepattern.match(self.cleaned_data['AccountantName']):
            raise forms.ValidationError("Enter proper Accountant Name")

        if not namepattern.match(self.cleaned_data['CorrespondentName']):
            raise forms.ValidationError("Enter proper Correspondent Name")
        
        if not mobilepattern.match(self.cleaned_data['AccountantMobile']):
            raise forms.ValidationError("Enter proper Accountant MobileNo")

        if not mobilepattern.match(self.cleaned_data['AccountantWhatsAppNo']):
            raise forms.ValidationError("Enter proper Accountant WhatsAppNo")

        if not mobilepattern.match(self.cleaned_data['CorrespondentMobile']):
            raise forms.ValidationError("Enter proper Correspondent MobileNo")

        if not mobilepattern.match(self.cleaned_data['CorrespondentWhatsAppNo']):
            raise forms.ValidationError("Enter proper Correspondent WhatsAppNo")


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model=sm.Students
        fields=['StudentName','Gender','StudentDOB','StudentMobileNo','Class','FatherName','MotherName','GaurdianName']
    
    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['StudentName']):
            raise forms.ValidationError("Enter proper Student name")

        if not namepattern.match(self.cleaned_data['FatherName']):
            raise forms.ValidationError("Enter proper Father name")

        if not namepattern.match(self.cleaned_data['MotherName']):
            raise forms.ValidationError("Enter proper Mother name")

        if not namepattern.match(self.cleaned_data['GaurdianName']):
            raise forms.ValidationError("Enter proper Gaurdian name")

        mobilepattern=re.compile("[0-9]{10}")
        if not mobilepattern.match(self.cleaned_data['StudentMobileNo']):
            raise forms.ValidationError("Enter proper Student mobile number")


class StudentForm(forms.ModelForm):
    class Meta:
        model = sm.Students   
        exclude = ['UserID','SchoolID','AdmissionNo','AdmissionID','Application','AdmissionDate','StudentPhoto','Religion','CasteCategory']

    def clean(self):
        namepattern=re.compile("^[a-zA-Z][a-zA-Z\s.]*$")
        if not namepattern.match(self.cleaned_data['StudentName']):
            raise forms.ValidationError("Enter proper Student name")

        mobilepattern=re.compile("[0-9]{10}")
        if not mobilepattern.match(self.cleaned_data['StudentMobileNo']):
            raise forms.ValidationError("Enter proper Student mobile number")


        if self.cleaned_data['FatherName'] != None:
            if not namepattern.match(self.cleaned_data['FatherName']):
                raise forms.ValidationError("Enter proper Father name")

            mobilepattern=re.compile("[0-9]{10}")
            if not mobilepattern.match(self.cleaned_data['FatherMobileNo']):
                raise forms.ValidationError("Enter proper Father mobile number")

            if not mobilepattern.match(self.cleaned_data['FatherWhatsappNo']):
                raise forms.ValidationError("Enter proper Father whatsapp number")

            if not namepattern.match(self.cleaned_data['FatherQualification']):
                raise forms.ValidationError("Enter proper Father qualification")

            if not namepattern.match(self.cleaned_data['FatherOccupation']):
                raise forms.ValidationError("Enter proper Father Occupation")

            if self.cleaned_data['FatherIncome']<0:
                raise forms.ValidationError("Father Income should be greater than Zero")

        if self.cleaned_data['MotherName'] != None:
            if not namepattern.match(self.cleaned_data['MotherName']):
                raise forms.ValidationError("Enter proper Mother name")

            mobilepattern=re.compile("[0-9]{10}")
            if not mobilepattern.match(self.cleaned_data['MotherMobileNo']):
                raise forms.ValidationError("Enter proper Mother mobile number")

            if not mobilepattern.match(self.cleaned_data['MotherWhatsappNo']):
                raise forms.ValidationError("Enter proper Mother whatsapp number")

            if not namepattern.match(self.cleaned_data['MotherQualification']):
                raise forms.ValidationError("Enter proper Mother qualification")

            if not namepattern.match(self.cleaned_data['MotherOccupation']):
                raise forms.ValidationError("Enter proper Mother Occupation")

            if self.cleaned_data['MotherIncome']<0:
                raise forms.ValidationError("Mother Income should be greater than Zero")

        if self.cleaned_data['GaurdianName'] != None:
            if not namepattern.match(self.cleaned_data['GaurdianName']):
                raise forms.ValidationError("Enter proper Gaurdian name")

            if not namepattern.match(self.cleaned_data['GaurdianQualification']):
                raise forms.ValidationError("Enter proper Gaurdian qualification")

            if not namepattern.match(self.cleaned_data['GaurdianOccupation']):
                raise forms.ValidationError("Enter proper Gaurdian Occupation")

            if self.cleaned_data['GaurdianIncome']<0:
                raise forms.ValidationError("Gaurdian Income should be greater than Zero")

            mobilepattern=re.compile("[0-9]{10}")
            if not mobilepattern.match(self.cleaned_data['GaurdianMobileNo']):
                raise forms.ValidationError("Enter proper Gaurdian mobile number")

            if not mobilepattern.match(self.cleaned_data['GaurdianWhatsappNo']):
                raise forms.ValidationError("Enter proper Gaurdian whatsapp number")
            

class AssignFeeAmountForm(forms.ModelForm):
    class Meta:
        model=sm.AssignFeeAmount
        fields=['Class','SubFee','FeesType','Amount']

class CollectFeeForm(forms.ModelForm):
    class Meta:
        model=sm.CollectFee
        exclude=['CollectFeeID','CollectFeeDate','Admission','AssignClass','School','Bank','PaymentStatus','Online','CollectFeeNo','RefferenceNO']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model=sm.Attendance
        exclude=['AttendanceID','StudentID','AttendanceDate','Present','Halfday','Absent']