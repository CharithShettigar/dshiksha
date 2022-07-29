from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # path('login', views.login_form, name="login"),
    path('Dashboard/AdminData', views.dashboard, name="dashboard"),

    path('',views.index,name='index'),
    
    path('accounts/login/', views.login_view, name="login_view"),
    path('accounts/logout', views.logout_form, name="logout"),
    path('accounts/login', views.login_view, name="login"),


    path('Dashboard/AdminData', views.dashboard, name="dashboard"),

    # settings
    path('Settings/AddState', views.add_state, name="add_state"),
    path('Settings/AddAcademicYear', views.add_academic_year, name="add_academic_year"),
    path('Settings/AddParish', views.add_parish, name="add_parish"),
    path('Settings/AddGender', views.add_gender, name="add_gender"),
    path('Settings/AddNationality', views.add_nationality, name="add_nationality"),
    path('Settings/AddMotherTongue', views.add_mother_tongue, name="add_mother_tomgue"),
    path('Settings/AddBloodGroup', views.add_blood_group, name="add_blood_group"),
    path('Settings/AddReligion', views.add_religion, name="add_religion"),
    path('Settings/AddPostOffice', views.add_post_office, name="add_post_office"),
    path('Settings/AddMediumOfInstruction', views.add_medium_of_instruction, name="add_medium_of_instruction"),
    path('Settings/AddDesignation', views.add_designation, name="add_designation"),
    path('Settings/AddSubject', views.add_subject, name="add_subject"),
]
