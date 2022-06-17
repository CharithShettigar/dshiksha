from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # path('login', views.login_form, name="login"),
    path('Dashboard/AdminData', views.dashboard, name="dashboard"),

    # ACCOUNTS PATH
    path('accounts/login/', views.login_view, name="login_view"),
    path('accounts/logout', views.logout_form, name="logout"),
    path('accounts/login', views.login_view, name="login"),

    # ERP SETTINGS PATH
    path('Settings/AddState', views.add_state, name="add_state"),
    path('Settings/AddAcademicYear', views.add_academic_year, name="add_academic_year"),
    path('Settings/AddParish', views.add_parish, name="add_parish"),
    path('Settings/AddGender', views.add_gender, name="add_gender"),
    path('Settings/AddNationality', views.add_nationality, name="add_nationality"),
    path('Settings/AddMotherTongue', views.add_mother_tongue, name="add_mother_tomgue"),
    path('Settings/AddBloodGroup', views.add_blood_group, name="add_blood_group"),
    path('Settings/AddStaffQualification', views.add_staff_qualification, name="add_staff_qualification"),
    path('Settings/AddReligion', views.add_religion, name="add_religion"),
    path('Settings/AddExtras', views.add_extras, name="add_extras"),
    path('Settings/CreateClass', views.add_class, name="add_class"),
    path('Settings/ClassLevelFees', views.add_class_level_fees, name="class_level_fees"),
    path('Settings/AddPostOffice', views.add_post_office, name="add_post_office"),
    path('Settings/AddDesignation', views.add_designation, name="add_designation"),
    path('Settings/AddModeOfTransport', views.add_mode_of_transport, name="add_mode_of_transport"),
    path('Settings/AddMediumOfInstruction', views.add_medium_of_instruction, name="add_medium_of_instruction"),
    path('Settings/AddSchoolAffiliation', views.add_school_affiliation, name="add_school_affiliation"),
    path('Settings/AddNatureOfAppointment', views.add_nature_of_appointment, name="add_nature_of_appointment"),
    path('Settings/CreateSchoolType', views.create_school_type, name="create_school_type"),
    path('Settings/CreateArea', views.create_area, name="create_area"),
    path('Settings/CreateInstitutionLevel', views.create_institution_level, name="create_institution_level"),
    path('Settings/CreateSyllabusType', views.create_syllabus_type, name="create_syllabus_type"),
    path('Settings/CreatePaymentMode', views.create_payment_mode, name="create_payment_mode"),
    path('Settings/CreateCorrespondent', views.create_correspondent, name="create_correspondent"),
    path('Settings/CreateFeesType', views.create_fees_type, name="create_fees_type"),
    path('Settings/CreateSubFeesType', views.create_sub_fee_type, name="create_sub_fee_type"),
]
