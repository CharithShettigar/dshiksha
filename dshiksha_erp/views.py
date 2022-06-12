from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from .forms import UserForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'dshiksha_erp/index.html')

# def login_view(request):
#     return render(request,'dshiksha_erp/login.html')


def login_view(request):
    # without redirect
    context={
        'form':UserForm,
    }
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Wrong Credentials")
            return redirect('login')
    else:
        return render(request,'dshiksha_erp/login.html',context)


    # with redirect
    # if not request.user.is_authenticated:
    #     if request.method == 'POST':
    #         form = UserForm(request.POST)
    #         if form.is_valid():
    #             username=request.POST['username']
    #             password=request.POST['password']
    #             user=auth.authenticate(username=username,password=password)
    #             if user is None:
    #                 messages.error(request, "Invalid Credentials")
    #                 return redirect("login")
    #                 # return redirect("login/?redirect_to=" + form.data['redirect_to_url'])
    #             elif user.is_superuser:
    #                 auth.login(request, user)
    #                 return redirect('/')
    #                 # return redirect(form.data['redirect_to_url'])
    #             else:
    #                 messages.error(request, "You donot have access to this page")
    #                 return redirect("login")
    #                 # return redirect("login/?redirect_to=" + form.data['redirect_to_url'])
    #         else:
    #             # redirect_url = form.data['redirect_to_url']
    #             print(form.errors)
    #             messages.error(request, form.errors)
    #             return redirect("login")
    #             # return redirect("login/?redirect_to=" + redirect_url)
    #     else:
    #         # if request.GET.get('redirect_to') is None:
    #         #     redirect_url = "/"
    #         # else:
    #         #     redirect_url = request.GET.get('redirect_to')
    #         form = UserForm()
            
    #     context = {
    #         "form": form,
    #         # "redirect_url": redirect_url,
    #     }
    #     return render(request, 'dshiksha_erp/login.html', context)
    # else:
    #     return redirect("/")


def logout_form(request):
    auth.logout(request)
    return redirect('login')

