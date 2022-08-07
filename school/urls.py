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

    # Application
    path('Application/AssignApplicationFees', views.assign_application_fees, name="school_assign_application_fees"),
    path('Application/NewApplication', views.student_application, name="school_student_application"),
    path('Application/NewApplicationShow/<str:application_ID>', views.application_info_show, name="school_application_info_show"),

    # Staff Paths
    path('Staff/CreateStaff', views.create_staff, name="school_create_staff"),
    path('Staff/StaffInfo', views.staff_info, name="school_staff_info"),
    path('Staff/StaffInfoShow/<str:staff_ID>', views.staff_info_show, name="school_staff_info_show"),


    
]