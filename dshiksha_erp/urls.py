from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login_view,name='login'),

]