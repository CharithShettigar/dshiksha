from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from main.models import User, UserTypes
import dshiksha_erp.forms as fm
from django.contrib import messages

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/?redirect_to=/')
    else:
        if request.user.is_superuser:
            return redirect("Dashboard/AdminData")

# Route for Dashboard page
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'dshiksha_erp/pages/dashboard.html')
        # return render(request, 'dshiksha_erp/Pages/dashboard.html')
    else:
        return redirect("/")



def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = fm.LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(request, username=login_form.cleaned_data['Email'],
                                    password=login_form.cleaned_data['Password'])
                if user is None:
                    messages.error(request, "Invalid Credentials")
                    return redirect("/accounts/login/?redirect_to=" + login_form.data['redirect_to_url'])
                elif user.is_superuser:
                    login(request, user)
                    return redirect(login_form.data['redirect_to_url'])
                else:
                    messages.error(request, "You donot have access to this page")
                    return redirect("/accounts/login/?redirect_to=" + login_form.data['redirect_to_url'])
            else:
                redirect_url = login_form.data['redirect_to_url']
                print(login_form.errors)
                return redirect("/accounts/login/?redirect_to=" + redirect_url)
        else:
            if request.GET.get('redirect_to') is None:
                redirect_url = "/"
            else:
                redirect_url = request.GET.get('redirect_to')
            login_form = fm.LoginForm()
            
        context = {
            "login_form": login_form,
            "redirect_url": redirect_url,
        }
        return render(request, 'dshiksha_erp/login.html', context)
    else:
        return redirect("/Dashboard/AdminData")

# def login_view(request):
#     # without redirect
#     context={
#         'form':UserForm,
#     }
#     if request.method=='POST':
#         username=request.POST['username']
#         password=request.POST['password']
#         user=auth.authenticate(username=username,password=password)

#         if user is not None:
#             auth.login(request,user)
#             return redirect('/')
#         else:
#             messages.info(request,"Wrong Credentials")
#             return redirect('login')
#     else:
#         return render(request,'dshiksha_erp/login.html',context)

def logout_form(request):
    logout(request)
    return redirect('login?redirect_to=/')


