from django import forms
from main.models import User
from school import models as cbm
from dshiksha_erp import models as md

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['Email']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['Password'] = forms.CharField(widget=forms.PasswordInput)

    # def clean(self) :
    #     pass
