from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'dshiksha_erp/index.html')

def login_view(request):
    return render(request,'dshiksha_erp/login.html')