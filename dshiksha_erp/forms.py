from django import forms
from main.models import User
from . import models as md


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
        # if md.AcademicYear.objects.filter(OrderID = self.cleaned_data['OrderID']).exists():
        #     raise forms.ValidationError("Order ID already taken")

class StateForm(forms.ModelForm):
    class Meta:
        model = md.State
        fields = ['StateName']

    def clean(self):
        if md.State.objects.filter(StateName = self.cleaned_data['StateName']).exists():
            raise forms.ValidationError('State already exists')


class DistrictForm(forms.ModelForm):
    class Meta:
        model = md.District
        fields = ['DistrictName']

    def clean(self):
        if md.District.objects.filter(DistrictName = self.cleaned_data['DistrictName'], State = md.State.objects.get(StateID = self.cleaned_data['State'].StateID)).exists():
            raise forms.ValidationError('District already exists')

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
        if md.Taluk.objects.filter(TalukName = self.cleaned_data['TalukName'], District = md.District.objects.get(DistrictID = self.cleaned_data['DistrictName'].DistrictID)).exists():
            raise forms.ValidationError('Taluk already exists')


class VillageForm(forms.ModelForm):
    class Meta:
        model = md.Village
        fields = ['VillageName']
    
    def __init__(self, *args, **kwargs):
        super(VillageForm, self).__init__(*args, **kwargs)
        self.fields['TalukName'] = forms.ModelChoiceField(queryset=md.Taluk.objects.all())

    def clean(self):
        print(self.cleaned_data)
        if md.Village.objects.filter(VillageName = self.cleaned_data['VillageName'], Taluk = md.Taluk.objects.get(TalukID = self.cleaned_data['TalukName'].TalukID)).exists():
            raise forms.ValidationError('Village already exists')


class GenderForm(forms.ModelForm):
    class Meta:
        model = md.Gender
        fields = ['GenderName', 'GenderOrder']


class NationalityForm(forms.ModelForm):
    class Meta:
        model = md.Nationality
        fields = ['NationalityName', 'CountryCode' ]

    
class MotherTongueForm(forms.ModelForm):
    class Meta:
        model = md.MotherTongue
        fields = ['MotherTongueName']

    def clean(self):
        if md.MotherTongue.objects.filter(MotherTongueName = self.cleaned_data['MotherTongueName'].capitalize()).exists():
            raise forms.ValidationError('Mother Tongue already exists')
    

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


class ReligionForm(forms.ModelForm):
    class Meta:
        model = md.Religion
        fields = ['ReligionName']

    def clean(self):
        if md.Religion.objects.filter(ReligionName = self.cleaned_data['ReligionName'].capitalize()).exists():
            raise forms.ValidationError('Religion already exists')

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



class DesignationForm(forms.ModelForm):
    class Meta:
        model = md.Designation
        fields = ['DesignationName']

    def clean(self):
        if md.Designation.objects.filter(DesignationName=self.cleaned_data['DesignationName'].capitalize()).exists():
            raise forms.ValidationError('Designation already exists')

class StaffSubjectForm(forms.ModelForm):
    class Meta:
        model = md.StaffSubject
        fields = ['StaffSubjectName']

    def clean(self):
        if md.StaffSubject.objects.filter(StaffSubjectName = self.cleaned_data['StaffSubjectName'].capitalize(

        )).exists():
            raise forms.ValidationError('Staff Subject already exists')


class MediumOfInstructionForm(forms.ModelForm):
    class Meta:
        model = md.MediumOfInstruction
        fields = ['MediumOfInstruction']