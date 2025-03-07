from django.urls import include, path
from . import views
from . import update_views

from django.conf import settings
from django.conf.urls.static import static


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
    path('Application/NewApplicationShow/<str:application_ID>', views.application_info_show,name="school_application_info_show"),

    # Admission
    path('Admission/NewAdmission', views.student_admission, name="school_student_admission"),

    #student
    path('Student/StudentShow/<str:student_id>', views.student_info_show, name="school_student_info_show"),

    # Attendance
    path('Attendance/MarkAttendance', views.mark_attendance, name="student_mark_attendance"),
    path('Attendance/ReportAttendance', views.attendance_list, name="student_attendance_info"),
    path('Attendance/StudentAttendanceShow/<str:student_id>', views.student_attendance_show, name="student_attendance_info"),


    # Staff Paths
    path('Staff/CreateStaff', views.create_staff, name="school_create_staff"),
    path('Staff/StaffInfo', views.staff_info, name="school_staff_info"),
    path('Staff/StaffInfoShow/<str:staff_ID>', views.staff_info_show, name="school_staff_info_show"),
    
    # Fees
    path('Fees/AssignFeeAmount', views.assign_fee_amount, name="assign_fee_amount"),
    path('Fees/CollectFee', views.collect_fee, name="collect_fee"),
    path('Fees/StudnetCollectFee/<str:student_id>', views.collect_fee_student, name="collect_fee_student"),
    path('Fees/ShowCollectFee/<str:student_id>', views.fee_info_show,name="fee_info_show"),

    # Print Reciept
    path('PrintFees/<str:student_id>', views.fees_reciept_pdf,name="fee_reciept"),


    #update the information
    path('Update/UpdateSchoolInfo/<str:school_id>',update_views.update_school,name="update_school_info"),
    path('Update/UpdateStaffInfo/<str:staff_id>',update_views.update_staff,name="update_staff_info"),
    path('Update/UpdateStudentInfo/<str:student_id>',update_views.update_student,name="update_student_info"),

    #Delete the information
    path('DeleteStaffInfo/<str:staff_id>',views.delete_staff,name="delete_staff_info"),
    path('DeleteStudentInfo/<str:student_id>',views.delete_student,name="delete_student_info"),

    #Feedback from school
    path('Feedback/FeedbackInfo',views.feedback_info,name="feedback_info"),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

