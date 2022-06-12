from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_form,name='logout'),
    path('admin/', admin.site.urls),
]