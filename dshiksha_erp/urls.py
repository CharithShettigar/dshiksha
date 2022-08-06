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
    path('Settings/AddNationality', views.add_nationality, name="add_nationality"),
    path('Settings/AddMotherTongue', views.add_mother_tongue, name="add_mother_tomgue"),
    path('Settings/AddReligion', views.add_religion, name="add_religion"),
    path('Settings/AddPostOffice', views.add_post_office, name="add_post_office"),
    
    #School
    path('School/AddDesignation', views.add_designation, name="add_subject"),
    path('School/CreateClass', views.add_class, name="add_class"),
    path('School/AssignClassLevel', views.cbse_assign_class_level, name="cbse_assign_class_level"),
    path('School/create_school', views.create_school, name="create_school"),
    path('School/CreateInstitutionLevel', views.create_institution_level, name="create_institution_level"),
    path('School/AddSchoolAffiliation', views.add_school_affiliation, name="add_school_affiliation"),
    path('School/AddStaffQualification', views.add_staff_qualification, name="add_staff_qualification"),
]
