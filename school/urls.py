from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path('accounts/logout', views.logout_view, name='logout'),

    path('Dashboard', views.dashboard, name="school_dashboard"),


    # School Paths
    path('School/SchoolInfo', views.school_info, name="school_school_info"),
    path('School/AssignClass', views.assign_class, name="school_assign_class"),
    path('School/AssignApplicationFees', views.assign_application_fees, name="school_assign_application_fees"),
    # path('School/NewApplication', views.student_application, name="school_student_application"),

    
]