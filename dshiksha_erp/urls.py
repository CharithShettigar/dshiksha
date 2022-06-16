from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),


    path('',views.index,name='index'),
    
    path('accounts/login/', views.login_view, name="login_view"),
    path('accounts/logout', views.logout_form, name="logout"),
    path('accounts/login', views.login_view, name="login"),


    path('Dashboard/AdminData', views.dashboard, name="dashboard"),
]