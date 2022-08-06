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
        fields = ['StaffName', 'StaffEmailID', 'StaffMobile']
        # exclude = ['UserID']
        # fields = ['StaffName', 'StaffEmailID', 'StaffMobile','DOB','Gender','BloodGroup','MaritalStatus','Caste','MotherTongue','AddressLine1','AddressLine2']

    def __init__(self, *args, **kwaargs):
        super(StaffCreateForm, self).__init__(*args, **kwaargs)
        self.fields['Password'] = forms.CharField(widget=forms.PasswordInput)
        self.fields['PasswordConfirm'] = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        if self.cleaned_data['Password'] != self.cleaned_data['PasswordConfirm']:
            raise forms.ValidationError("Password does not match")

class ApplicationFeesForm(forms.ModelForm):
    class Meta:
        model = sm.ApplicationNo
        fields = ['Amount']

    def __init__(self, *args, **kwaargs):
        super(ApplicationFeesForm, self).__init__(*args, **kwaargs)
        self.fields['Amount'] = forms.CharField()
        self.fields['ApplicationNoID'] = forms.ModelChoiceField(queryset=sm.ApplicationNo.objects.all())


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = sm.Application
        fields = ['StudentName','Gender','StudentDOB','StudentMobileNo','ParentName', 'ParentMobileNo','Class','Amount','ModeOfPayment']
