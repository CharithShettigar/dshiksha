
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import dshiksha_erp.models as md
import uuid
import dshiksha_erp.forms as fm
import school.models as sm
from main.models import User, UserTypes

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/?redirect_to=/')
    else:
        if request.user.is_superuser:
            return redirect("Dashboard/AdminData")


# Route for Dashboard page
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {
        "school_count":sm.School.objects.all().count(),
        "state_count":md.State.objects.all().count(),
        "district_count":md.District.objects.all().count(),
        "village_count":md.Village.objects.all().count(),
        "taluk_count":md.Taluk.objects.all().count(),
        "area_count":md.Area.objects.all().count(),
        "staff_count":sm.Staff.objects.all().count(),
        "student_count":sm.Students.objects.all().count(),
        "student_boys_count":sm.Students.objects.filter(Gender__GenderName ='Male').count(),
        "student_girls_count":sm.Students.objects.filter(Gender__GenderName ='Female').count(),
        "staff_boys_count":sm.Staff.objects.filter(Gender__GenderName ='Male').count(),
        "staff_girls_count":sm.Staff.objects.filter(Gender__GenderName ='Female').count(),
        }
        return render(request, 'dshiksha_erp/Pages/dashboard.html',context)
    else:
        return redirect("/")


# Login View
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            redirect_url = ""
            login_form = fm.LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(request, username=login_form.cleaned_data['Email'],password=login_form.cleaned_data['Password'])
                if user is None:
                    messages.error(request, "Invalid Credentials")
                    print("***********Invalid credential************")
                    return redirect("/accounts/login/?redirect_to=" + login_form.data['redirect_to_url'])
                elif user.is_superuser:
                    login(request, user)
                    return redirect(login_form.data['redirect_to_url'])
                else:
                    messages.error(request, "You do not have access to this page")
                    return redirect("/accounts/login/?redirect_to=" + login_form.data['redirect_to_url'])
            else:
                redirect_url = login_form.data['redirect_to_url']
                print(login_form.errors)
                messages.error(request, "Email does not exist")
                return redirect("/accounts/login/?redirect_to=" + redirect_url)
        else:
            if request.GET.get('redirect_to') is None:
                redirect_url = "/"
            else:
                redirect_url = request.GET.get('redirect_to')
            login_form = fm.LoginForm()
            
        context = {
            "login_form": login_form,
            "redirect_url": redirect_url,
        }
        return render(request, 'dshiksha_erp/login.html', context)
    else:
        return redirect("/Dashboard/AdminData")


# Logout form
def logout_form(request):
    logout(request)
    return redirect('login?redirect_to=/')

def add_state(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            state_form = fm.StateForm(request.POST)
            district_form = fm.DistrictForm(request.POST)
            taluk_form = fm.TalukForm(request.POST)
            village_form = fm.VillageForm(request.POST)
            if request.POST.get("form-type") == 'add-state':
                if state_form.is_valid():
                    md.State(StateID=uuid.uuid4(), StateName=state_form.cleaned_data['StateName'].capitalize()).save()
                    return redirect("/Settings/AddState")
                else:
                    print("Error in state form")
            elif request.POST.get("form-type") == 'add-district':
                if district_form.is_valid():
                    md.District(DistrictID=uuid.uuid4(),
                                DistrictName=district_form.cleaned_data['DistrictName'].capitalize(),
                                State=district_form.cleaned_data['State']).save()
                    return redirect("/Settings/AddState")
                else:
                    print("error while submitting the district form")
            elif request.POST.get("form-type") == 'add-taluk':
                if taluk_form.is_valid():
                    md.Taluk(TalukID=uuid.uuid4(), TalukName=taluk_form.cleaned_data['TalukName'].capitalize(),
                             District=taluk_form.cleaned_data['DistrictName']).save()
                    return redirect("/Settings/AddState")
                else:
                    print("error while submitting the taluk form")
            elif request.POST.get("form-type") == 'add-village':
                if village_form.is_valid():
                    md.Village(VillageID=uuid.uuid4(),
                               VillageName=village_form.cleaned_data['VillageName'].capitalize(),
                               Taluk=village_form.cleaned_data['TalukName']).save()
                    return redirect("/Settings/AddState")
                else:
                    print("error while submitting the village form")
        else:
            state_form = fm.StateForm()
            district_form = fm.DistrictForm()
            taluk_form = fm.TalukForm()
            village_form = fm.VillageForm()
        state_list = md.State.objects.all()
        district_list = md.District.objects.all()
        taluk_list = md.Taluk.objects.all()
        village_list = md.Village.objects.all()
        context = {
            "state_form": state_form,
            "district_form": district_form,
            "taluk_form": taluk_form,
            "village_form": village_form,
            "state_list": state_list,
            "district_list": district_list,
            "taluk_list": taluk_list,
            "village_list": village_list,
        }
        return render(request, 'dshiksha_erp/Pages/Settings/add_state.html', context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddState")

# admin 
# def create_superuser(request):
    # if request.user.is_authenticated:
    #     if request.method == 'POST':
    #         superuer_form = fm.SchoolForm(request.POST)
    #         if school_school_form.is_valid():
    #             if sm.School.objects.filter(SchoolName=school_school_form.cleaned_data['SchoolName'],
    #                                          Email=school_school_form.cleaned_data['Email']).exists():
    #                 messages.error(request, "School Already Present")
    #             elif sm.School.objects.filter(SchoolName=school_school_form.cleaned_data['SchoolName']).exists():
    #                 messages.error(request, "School Name already present")
    #             elif sm.School.objects.filter(Email=school_school_form.cleaned_data['Email']).exists():
    #                 messages.error(request, "School Email already present")
    #             elif sm.School.objects.filter(SchoolCode=school_school_form.cleaned_data['SchoolCode']).exists():
    #                 messages.error(request, "School Code already present")
    #             elif sm.School.objects.filter(SchoolUsername=school_school_form.cleaned_data['SchoolUsername']).exists():
    #                 messages.error(request, "School Username already present")
    #             else:
    #                 user = User.objects.create_user(email=school_school_form.cleaned_data['Email'],
    #                                                 first_name=school_school_form.cleaned_data['SchoolName'],
    #                                                 username=school_school_form.cleaned_data['SchoolCode'],
    #                                                 password=school_school_form.cleaned_data['Password'],
    #                                                 UserType=UserTypes.objects.get(UserTypeName="School").UserTypeID)
    #                 redirect("/School/create_school")
    #         else:
    #             print(school_school_form.errors)
    #     else:
    #         school_school_form = fm.SchoolForm()
    #     context = {
    #         "school_form": school_school_form,
    #         "village_list": md.Village.objects.all(),
    #         "post_office_list": md.PostOffice.objects.all(),
    #         "school_list": sm.School.objects.all(),
    #         "academic_year_list": md.AcademicYear.objects.all(),
    #     }
    #     return render(request, "dshiksha_erp/Pages/School/create_school.html", context)
    # else:
    #     return redirect("/accounts/login/?redirect_to=/School/create_school")

def add_academic_year(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            academic_year_form = fm.AcademicYearForm(request.POST)
            if academic_year_form.is_valid():
                if md.AcademicYear.objects.filter(OrderID=academic_year_form.cleaned_data['OrderID']).exists():
                    messages.error(request, "Order ID Already exists")
                else:
                    print(academic_year_form.cleaned_data)
                    if academic_year_form.cleaned_data['IsActive'] == True:
                        for d in md.AcademicYear.objects.all():
                            d.IsActive = False
                            d.save()
                    
                    md.AcademicYear(AcademicYearID=uuid.uuid4(),
                                    AcademicYear=academic_year_form.cleaned_data['AcademicYear'].capitalize(),
                                    OrderID=academic_year_form.cleaned_data['OrderID'], IsActive = academic_year_form.cleaned_data['IsActive']).save()
                    return redirect("/Settings/AddAcademicYear")
            else:
                print("Error while submitting the academic year form")
                print(academic_year_form.errors)
        else:
            academic_year_form = fm.AcademicYearForm(initial = {'OrderID' : md.AcademicYear.objects.count() + 1})
        academic_year_list = md.AcademicYear.objects.all().order_by("OrderID")
        context = {
            "academic_year_form": academic_year_form,
            "academic_year_list": academic_year_list,
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_academic_year.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddAcademicYear")

def add_nationality(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nationality_form = fm.NationalityForm(request.POST)
            if nationality_form.is_valid():
                if md.Nationality.objects.filter(CountryCode=nationality_form.cleaned_data['CountryCode']).exists():
                    messages.error(request, "Country Code exists already")
                elif md.Nationality.objects.filter(
                        NationalityName=nationality_form.cleaned_data['NationalityName']).exists():
                    messages.error(request, "Nationality Already present")
                else:
                    md.Nationality(NationalityID=uuid.uuid4(),
                                   NationalityName=nationality_form.cleaned_data['NationalityName'].capitalize(),
                                   CountryCode=nationality_form.cleaned_data['CountryCode'].upper()).save()
                    return redirect("/Settings/AddNationality")
            else:
                print("Something went wrong while adding the nationality data")
        else:
            nationality_form = fm.NationalityForm()
        nationality_list = md.Nationality.objects.all()

        context = {
            "nationality_form": nationality_form,
            "nationality_list": nationality_list,
        }

        return render(request, "dshiksha_erp/Pages/Settings/add_nationality.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddNationality")

def create_area(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            area_form = fm.AreaForm(request.POST)
            if area_form.is_valid():
                if md.Area.objects.filter(AreaType = area_form.cleaned_data['AreaType']).exists():
                    messages.error(request, "Area Already exists")
                else:
                    md.Area(AreaID = uuid.uuid4(), AreaType = area_form.cleaned_data['AreaType']).save()
                    return redirect("/Settings/CreateArea")
            else:
                print(area_form.errors)
        else:
            area_form = fm.AreaForm()
        context = {
            "area_form": area_form,
            "area_list": md.Area.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/create_area.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreateArea")

def add_mother_tongue(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            mother_tongue_form = fm.MotherTongueForm(request.POST)
            if mother_tongue_form.is_valid():
                md.MotherTongue(MotherTongueID=uuid.uuid4(), MotherTongueName=mother_tongue_form.cleaned_data[
                    'MotherTongueName'].capitalize()).save()
                return redirect("/Settings/AddMotherTongue")
        else:
            mother_tongue_form = fm.MotherTongueForm()
        context = {
            "mother_tongue_form": mother_tongue_form,
            "mother_tongue_list": md.MotherTongue.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_mother_tongue.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddMotherTongue")

def add_religion(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            religion_form = fm.ReligionForm(request.POST)
            caste_category_form = fm.CasteCategoryForm(request.POST)
            caste_form = fm.CasteForm(request.POST)
            if request.POST.get('form-type') == 'religion-form':
                if religion_form.is_valid():
                    md.Religion(ReligionID=uuid.uuid4(),
                                ReligionName=religion_form.cleaned_data['ReligionName'].capitalize()).save()
                    return redirect("/Settings/AddReligion")
                else:
                    print("Something went wrong while adding the religion data")
            elif request.POST.get('form-type') == 'caste-category-form':
                if caste_category_form.is_valid():
                    md.CasteCategory(CasteCategoryID=uuid.uuid4(), CasteCategoryName=caste_category_form.cleaned_data[
                        'CasteCategoryName'].capitalize()).save()
                    return redirect("/Settings/AddReligion")
                else:
                    print("Something went wrong while adding the caste category data")
            elif request.POST.get('form-type') == 'caste-form':
                if caste_form.is_valid():
                    if md.Caste.objects.filter(CasteName=caste_form.cleaned_data['CasteName']).exists():
                        messages.error(request, "Caste already exists")
                    else:
                        md.Caste(CasteID=uuid.uuid4(), CasteName=caste_form.cleaned_data['CasteName'].capitalize(),
                                 CasteCategory=caste_form.cleaned_data['CasteCategory'],
                                 Religion=caste_form.cleaned_data['Religion']).save()
                        return redirect("/Settings/AddReligion")
                else:
                    print("Something went wrong while adding new caste data")
                    print(caste_form.errors)
        else:
            religion_form = fm.ReligionForm()
            caste_category_form = fm.CasteCategoryForm()
            caste_form = fm.CasteForm()
        context = {
            "religion_form": religion_form,
            "caste_form": caste_form,
            "caste_category_form": caste_category_form,
            "religion_list": md.Religion.objects.all(),
            "caste_category_list": md.CasteCategory.objects.all(),
            "caste_list": md.Caste.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_religion.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddReligion")

def add_post_office(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_office_form = fm.PostOfficeForm(request.POST)
            if post_office_form.is_valid():
                if md.PostOffice.objects.filter(
                        PostOfficeName=post_office_form.cleaned_data['PostOfficeName']).exists():
                    messages.error(request, "Post Office already exists")
                elif md.PostOffice.objects.filter(Pincode=post_office_form.cleaned_data['Pincode']).exists():
                    messages.error(request, "Pincode already exists")
                else:
                    md.PostOffice(PostOfficeID=uuid.uuid4(),
                                  PostOfficeName=post_office_form.cleaned_data['PostOfficeName'].capitalize(),
                                  Pincode=post_office_form.cleaned_data['Pincode']).save()
                    return redirect("/Settings/AddPostOffice")
        else:
            post_office_form = fm.PostOfficeForm()
        context = {
            "post_office_form": post_office_form,
            "post_office_list": md.PostOffice.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_post_office.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddPostOffice")

# Create Designation
def add_designation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            designation_form = fm.DesignationForm(request.POST)
            staff_subject_form = fm.StaffSubjectForm(request.POST)
            if request.POST.get('form-type') == "designation-form":
                if designation_form.is_valid():
                    md.Designation(DesignationID=uuid.uuid4(),
                                   DesignationName=designation_form.cleaned_data['DesignationName'].capitalize()).save()
                    return redirect("/Staff/AddDesignation")
            elif request.POST.get('form-type') == 'staff-subject-form':
                if staff_subject_form.is_valid():
                    md.StaffSubject(StaffSubjectID=uuid.uuid4(), StaffSubjectName=staff_subject_form.cleaned_data[
                        'StaffSubjectName'].capitalize()).save()
                    return redirect("/Staff/AddDesignation")
        else:
            designation_form = fm.DesignationForm()
            staff_subject_form = fm.StaffSubjectForm()
        context = {
            "designation_form": designation_form,
            "designation_list": md.Designation.objects.all(),
            "staff_subject_form": staff_subject_form,
            "staff_subject_list": md.StaffSubject.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Staff/add_subject.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/AddDesignation")

# Create Subject
def add_subject(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            staff_subject_form = fm.StaffSubjectForm(request.POST)
            if request.POST.get('form-type') == 'staff-subject-form':
                if staff_subject_form.is_valid():
                    md.StaffSubject(StaffSubjectID=uuid.uuid4(), StaffSubjectName=staff_subject_form.cleaned_data[
                        'StaffSubjectName'].capitalize()).save()
                    return redirect("/School/AddSubject")
        else:
            staff_subject_form = fm.StaffSubjectForm()
        context = {
            "staff_subject_form": staff_subject_form,
            "staff_subject_list": md.StaffSubject.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/School/add_subject.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/AddSubject")

def create_school(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            school_school_form = fm.SchoolForm(request.POST)
            if school_school_form.is_valid():
                if sm.School.objects.filter(SchoolName=school_school_form.cleaned_data['SchoolName'],
                                             Email=school_school_form.cleaned_data['Email']).exists():
                    messages.error(request, "School Already Present")
                elif sm.School.objects.filter(SchoolName=school_school_form.cleaned_data['SchoolName']).exists():
                    messages.error(request, "School Name already present")
                elif sm.School.objects.filter(Email=school_school_form.cleaned_data['Email']).exists():
                    messages.error(request, "School Email already present")
                elif sm.School.objects.filter(SchoolCode=school_school_form.cleaned_data['SchoolCode']).exists():
                    messages.error(request, "School Code already present")
                elif sm.School.objects.filter(SchoolUsername=school_school_form.cleaned_data['SchoolUsername']).exists():
                    messages.error(request, "School Username already present")
                else:
                    user = User.objects.create_user(email=school_school_form.cleaned_data['Email'],
                                                    first_name=school_school_form.cleaned_data['SchoolName'],
                                                    username=school_school_form.cleaned_data['SchoolCode'],
                                                    password=school_school_form.cleaned_data['Password'],
                                                    UserType=UserTypes.objects.get(UserTypeName="School").UserTypeID)
                    school_data = sm.School(SchoolID=uuid.uuid4(),
                                            SchoolName=school_school_form.cleaned_data['SchoolName'].capitalize(),
                                            SchoolType="SCHOOL", Email=school_school_form.cleaned_data['Email'],
                                            Village=school_school_form.cleaned_data['Village'],
                                            Pincode=school_school_form.cleaned_data['Pincode'],
                                            UserID=User.objects.get(UserID=user.UserID),
                                            SchoolUsername=school_school_form.cleaned_data['SchoolUsername'],
                                            SchoolCode=school_school_form.cleaned_data['SchoolCode'],
                                            CurrentAcademicYear = school_school_form.cleaned_data['CurrentAcademicYear'], # Add academic Year support in web page
                                            Landline=school_school_form.cleaned_data['Landline'],
                                            
                                            SyllabusType=school_school_form.cleaned_data['SyllabusType'],
                                            
                                            AccountantName=school_school_form.cleaned_data['AccountantName'],
                                            AccountantEmail = school_school_form.cleaned_data['AccountantEmail'],
                                            AccountantMobile = school_school_form.cleaned_data['AccountantMobile'],
                                            AccountantWhatsAppNo = school_school_form.cleaned_data['AccountantWhatsAppNo'],

                                            CorrespondentFirstName = school_school_form.cleaned_data['CorrespondentFirstName'],
                                            CorrespondentLastName =school_school_form.cleaned_data['CorrespondentLastName'],
                                            CorrespondentEmail = school_school_form.cleaned_data['CorrespondentEmail'],
                                            CorrespondentMobile = school_school_form.cleaned_data['CorrespondentMobile'],
                                            CorrespondentWhatsAppNo = school_school_form.cleaned_data['CorrespondentWhatsAppNo'])#,
                                            #EstDate= cbse_school_form.cleaned_data['EstDate'])
                    school_data.save()
                    redirect("/School/create_school")
            else:
                print(school_school_form.errors)
        else:
            school_school_form = fm.SchoolForm()
        context = {
            "school_form": school_school_form,
            "village_list": md.Village.objects.all(),
            "post_office_list": md.PostOffice.objects.all(),
            "school_list": sm.School.objects.all(),
            "academic_year_list": md.AcademicYear.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/School/create_school.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/create_school")

def add_class(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            class_level_form = fm.ClassLevelForm(request.POST)
            class_list_form = fm.ClassListForm(request.POST)
            section_form = fm.SectionForm(request.POST)
            if request.POST.get("form-type") == "class-level-form":
                if class_level_form.is_valid():
                    if md.ClassLevel.objects.filter(ClassLevelName = class_level_form.cleaned_data['ClassLevelName']).exists():
                        messages.error(request, "Class Level already exists")
                    elif md.ClassLevel.objects.filter(ClassLevelCode = class_level_form.cleaned_data['ClassLevelCode'].upper()).exists():
                        messages.error(request,"Class Level Code already exists")
                    else:
                        md.ClassLevel(ClassLevelID = uuid.uuid4(), ClassLevelName = class_level_form.cleaned_data[
                            'ClassLevelName'], ClassLevelCode = class_level_form.cleaned_data['ClassLevelCode'].upper()).save()
                        return redirect("/School/CreateClass")
                else:
                    print(class_level_form.errors)
            elif request.POST.get("form-type") == "class-list-form":
                if class_list_form.is_valid():
                    if not md.ClassList.objects.filter(ClassName = class_list_form.cleaned_data['ClassName'].upper()).exists() and not md.ClassList.objects.filter(OrderID = class_list_form.cleaned_data['OrderID']).exists():
                        md.ClassList(ClassID=uuid.uuid4(), ClassName=class_list_form.cleaned_data['ClassName'].upper(), OrderID = class_list_form.cleaned_data['OrderID']).save()
                        return redirect("/School/CreateClass")
                    else:
                        messages.error(request, "Class Name already present")
            elif request.POST.get('form-type') == "section-form":
                if section_form.is_valid():
                    if not md.Section.objects.filter(SectionName = section_form.cleaned_data['SectionName'].upper()).exists():
                        md.Section(SectionID=uuid.uuid4(),
                                   SectionName=section_form.cleaned_data['SectionName'].upper()).save()
                        return redirect("/School/CreateClass")
                    else:
                        messages.error(request, "Section already present")
        else:
            class_list = md.ClassList.objects.all().order_by('OrderID')
            if md.ClassList.objects.last()==None:
                new_order_id=1
            else:
                new_order_id = class_list.last().OrderID + 1
            
            class_list_form = fm.ClassListForm(initial={'OrderID': new_order_id})
            class_level_form = fm.ClassLevelForm()
            section_form = fm.SectionForm()
        
        context = {
            "class_list_form": class_list_form,
            "class_level_form": class_level_form,
            "class_level_list": md.ClassLevel.objects.all(),
            "class_list": class_list,
            "section_form": section_form,
            "section_list": md.Section.objects.all(),
            }
        return render(request, "dshiksha_erp/Pages/School/add_class.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/CreateClass")

def school_assign_class_level(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            class_form = fm.ClassForm(request.POST)
            if class_form.is_valid():
                if sm.Class.objects.filter(ClassList = class_form.cleaned_data['ClassList'], ClassLevel = class_form.cleaned_data['ClassLevel']).exists():
                    messages.error(request, "Class already assigned")
                else:
                    sm.Class(ClassID=uuid.uuid4(), ClassList=class_form.cleaned_data['ClassList'],
                             ClassLevel=class_form.cleaned_data['ClassLevel']).save()
                    return redirect("/School/AssignClassLevel")
            else:
                print("Something went wrong")
                print(class_form.errors)
        else:
            class_form = fm.ClassForm()
        context = {
            "class_form": class_form,
            "class_list": sm.Class.objects.all().order_by('ClassList__OrderID',),
            "classes_list": md.ClassList.objects.all().order_by('OrderID'),
            "class_level_list": md.ClassLevel.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/School/assign_class_level.html", context)
    else:
        return redirect("/accounts/login/>redirect_to=/School/AssignClassLevel")

def create_institution_level(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            il_form = fm.InstitutionLevelForm(request.POST)
            if il_form.is_valid():
                if md.InstitutionLevel.objects.filter(InstitutionLevel = il_form.cleaned_data['InstitutionLevel']).exists():
                    messages.error(request, "Institution Level already exists")
                else:
                    md.InstitutionLevel(InstitutionLevelID = uuid.uuid4(), InstitutionLevel = il_form.cleaned_data['InstitutionLevel']).save()
                    return redirect("/School/CreateInstitutionLevel")
            else:
                print(il_form.errors)
        else:
            il_form = fm.InstitutionLevelForm()
        context = {
            "il_form": il_form,
            "il_list": md.InstitutionLevel.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/School/create_institution_level.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/CreateInstitutionLevel")

def add_staff_qualification(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            staff_qualification_form = fm.StaffQualificationForm(request.POST)
            if request.POST.get('form-type') == 'staff-qualification':
                if staff_qualification_form.is_valid():
                    md.StaffQualification(StaffQualificationID=uuid.uuid4(),
                                          StaffQualificationName=staff_qualification_form.cleaned_data[
                                              'StaffQualificationName']).save()
                    return redirect("/Staff/AddStaffQualification")
                else:
                    print("Something went wrong while adding the staff qualification data")
            else:
                print("something went wrong while adding the staff professional qualification data")
                print(staff_qualification_form.errors)
        else:
            staff_qualification_form = fm.StaffQualificationForm()
        context = {
            "staff_qualification_form": staff_qualification_form,
            "staff_qualification_list": md.StaffQualification.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Staff/add_staff_qualification.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Staff/AddStaffQualification")

def add_school_affiliation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sa_form = fm.SchoolAffiliationForm(request.POST)
            if sa_form.is_valid():
                if md.SchoolAffiliation.objects.filter(
                        SchoolAffiliation=sa_form.cleaned_data['SchoolAffiliation']).exists():
                    messages.error(request, "School Affiliation already exists")
                else:
                    md.SchoolAffiliation(SchoolAffiliationID=uuid.uuid4(),
                                         SchoolAffiliation=sa_form.cleaned_data['SchoolAffiliation']).save()
                    return redirect("/School/AddSchoolAffiliation")
            else:
                print(sa_form.errors)
        else:
            sa_form = fm.SchoolAffiliationForm()
        context = {
            "sa_form": sa_form,
            "sa_list": md.SchoolAffiliation.objects.all()
        }
        return render(request, "dshiksha_erp/Pages/School/add_school_affiliation.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/School/AddSchoolAffiliation")

# Fees Section
#Create Fees Types
def create_fees_type(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ft_form = fm.FeesTypeForm(request.POST)
            installment_form = fm.InstallmentForm(request.POST)

            if request.POST.get('form-type') == "fees-type-form":
                if ft_form.is_valid():
                    if not md.FeesType.objects.filter(FeesTypeName = ft_form.cleaned_data['FeesTypeName']).exists() and not md.FeesType.objects.filter(FeeTypeCode = ft_form.cleaned_data['FeeTypeCode']).exists():
                        md.FeesType(FeesTypeID = uuid.uuid4(), FeesTypeName = ft_form.cleaned_data['FeesTypeName'], FeeTypeCode = ft_form.cleaned_data['FeeTypeCode']).save()
                        return redirect("/Fees/CreateFeesType")
                    else:
                        print("Something went wrong")
                        messages.error(request, "Fees Type already exists")
                else:
                    print(ft_form.errors)
            elif request.POST.get("form-type") == "installment-form":
                if installment_form.is_valid():
                    if not md.Installment.objects.filter(InstallmentName = installment_form.cleaned_data['InstallmentName']).exists():
                        md.Installment(InstallmentID = uuid.uuid4(), InstallmentName = installment_form.cleaned_data['InstallmentName']).save()
                        return redirect("/Fees/CreateFeesType")
                    else:
                        messages.error(request, "Installment already exists")
                else:
                    print(installment_form.errors)
        else:
            ft_form = fm.FeesTypeForm()
            installment_form = fm.InstallmentForm()
        context = {
            "ft_form": ft_form,
            "ft_list": md.FeesType.objects.all(),
            "installment_form": installment_form,
            "installment_list": md.Installment.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Fees/create_fees_type.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Fees/create_fees_type")
        
#Create Sub Fees Type 
def create_sub_fee_type(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sft_form = fm.SubFeeForm(request.POST)
            if sft_form.is_valid():
                md.SubFee(SubFeeID=uuid.uuid4(), SubFeeName=sft_form.cleaned_data['SubFeeName'].capitalize(), FeesType=sft_form.cleaned_data['FeesType']).save()
                return redirect("/Fees/CreateSubFeesType")
            else:
                print("error while submitting the sub fee  form")
        else:
            sft_form = fm.SubFeeForm()
        context = {
            "sft_form": sft_form,
            "sft_list": md.SubFee.objects.all(),
            "fs_list": md.FeesType.objects.all().order_by('FeesTypeName'),
        }
        return render(request, 'dshiksha_erp/Pages/Fees/create_sub_fee_type.html', context)
    else:
        return redirect("/accounts/login/?redirect_to=/Fees/CreateSubFeesType")

def create_bank(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            bank_form = fm.BankForm(request.POST)
            online_form=fm.OnlineForm(request.POST)
            if request.POST.get('form-type') == "bank-form":
                if bank_form.is_valid():
                    if md.Bank.objects.filter(OrderID=bank_form.cleaned_data['OrderID']).exists():
                        messages.error(request, "Order ID Already exists")
                    else:
                        print(bank_form.cleaned_data)
                        md.Bank(BankID=uuid.uuid4(),BankName=bank_form.cleaned_data['BankName'].upper(),
                                    OrderID=bank_form.cleaned_data['OrderID']).save()
                        return redirect("/Fees/CreateBank")
                else:
                    print("Error while submitting the bank form")
                    print(bank_form.errors)

            elif request.POST.get('form-type')=="online-form":
                if online_form.is_valid():
                    if md.Online.objects.filter(OrderID=online_form.cleaned_data['OrderID']).exists():
                        messages.error(request, "Order ID Already exists")
                    else:
                        print(online_form.cleaned_data)
                        md.Online(OnlineID=uuid.uuid4(), OnlineAppName=online_form.cleaned_data['OnlineAppName'].upper(),OrderID=online_form.cleaned_data['OrderID']).save()
                        return redirect("/Fees/CreateBank")
                else:
                    print("Error while submitting the bank form")
                    print(online_form.errors)
        else:
            bank_form = fm.BankForm(initial = {'OrderID' : md.Bank.objects.count() + 1})
            bank_list = md.Bank.objects.all().order_by("OrderID")
            online_form = fm.OnlineForm(initial = {'OrderID' : md.Online.objects.count() + 1})
            online_list = md.Online.objects.all().order_by("OrderID")
        context = {
            "bank_form": bank_form,
            "bank_list": bank_list,
            "online_form": online_form,
            "online_list": online_list,
        }
        return render(request, "dshiksha_erp/Pages/Fees/create_bank.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Fees/CreateBank")
