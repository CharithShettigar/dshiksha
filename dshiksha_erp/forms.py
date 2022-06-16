from django import forms
from main.models import User


# class UserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=('username','password')


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