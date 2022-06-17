
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import dshiksha_erp.forms as fm
import dshiksha_erp.models as md
import school.models as cbm
from main.models import User, UserTypes
import uuid


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
        return render(request, 'dshiksha_erp/Pages/dashboard.html')
    else:
        return redirect("/")


# Login View
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = fm.LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(request, username=login_form.cleaned_data['Email'],
                                    password=login_form.cleaned_data['Password'])
                if user is None:
                    messages.error(request, "Invalid Credentials")
                    return redirect("/accounts/login/?redirect_to=" + login_form.data['redirect_to_url'])
                elif user.is_superuser:
                    login(request, user)
                    return redirect(login_form.data['redirect_to_url'])
                else:
                    messages.error(request, "You donot have access to this page")
                    return redirect("/accounts/login/?redirect_to=" + login_form.data['redirect_to_url'])
            else:
                redirect_url = login_form.data['redirect_to_url']
                print(login_form.errors)
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


# SETTING VIEWS
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


def add_parish(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            parish_form = fm.ParishForm(request.POST)
            if parish_form.is_valid():
                md.Parish(ParishID=uuid.uuid4(), ParishName=parish_form.cleaned_data['ParishName'],
                          ParishArea=parish_form.cleaned_data['ParishArea']).save()
                return redirect("/Settings/AddParish")
            else:
                print("Something went wrong while adding new parish")
        else:
            parish_form = fm.ParishForm()
        parish_list = md.Parish.objects.all()
        context = {
            "parish_form": parish_form,
            "parish_list": parish_list,
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_parish.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddParish")


def add_gender(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            gender_form = fm.GenderForm(request.POST)
            if gender_form.is_valid():
                if md.Gender.objects.filter(GenderOrder=gender_form.cleaned_data['GenderOrder']).exists():
                    messages.error(request, "Order Id exists")
                elif md.Gender.objects.filter(GenderName=gender_form.cleaned_data['GenderName']).exists():
                    messages.error(request, "Gender already present")
                else:
                    md.Gender(GenderID=uuid.uuid4(), GenderName=gender_form.cleaned_data['GenderName'].capitalize(),
                              GenderOrder=gender_form.cleaned_data['GenderOrder']).save()
                    return redirect("/Settings/AddGender")
        else:
            gender_form = fm.GenderForm()
        gender_list = md.Gender.objects.all().order_by("GenderOrder")
        context = {
            "gender_form": gender_form,
            "gender_list": gender_list,
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_gender.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddGender")


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


def add_blood_group(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            blood_group_form = fm.BloodGroupForm(request.POST)
            if blood_group_form.is_valid():
                md.BloodGroup(BloodGroupID=uuid.uuid4(),
                              BloodGroupName=blood_group_form.cleaned_data['BloodGroupName'].upper()).save()
                return redirect("/Settings/AddBloodGroup")
            else:
                print("Something went wrong while adding the blood group data")
        else:
            blood_group_form = fm.BloodGroupForm()
        context = {
            "blood_group_form": blood_group_form,
            "blood_group_list": md.BloodGroup.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_blood_group.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddBloodGroup")


def add_staff_qualification(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            staff_qualification_form = fm.StaffQualificationForm(request.POST)
            staff_pro_qualification_form = fm.StaffProQualificationForm(request.POST)
            if request.POST.get('form-type') == 'staff-qualification':
                if staff_qualification_form.is_valid():
                    md.StaffQualification(StaffQualificationID=uuid.uuid4(),
                                          StaffQualificationName=staff_qualification_form.cleaned_data[
                                              'StaffQualificationName']).save()
                    return redirect("/Settings/AddStaffQualification")
                else:
                    print("Something went wrong while adding the staff qualification data")
            elif request.POST.get('form-type') == 'staff-pro-qualification':
                if staff_pro_qualification_form.is_valid():
                    md.StaffProQualification(StaffProQualificationID=uuid.uuid4(),
                                             StaffProQualificationName=staff_pro_qualification_form.cleaned_data[
                                                 'StaffProQualificationName']).save()
                    return redirect("/Settings/AddStaffQualification")
            else:
                print("something went wrong while adding the staff professional qualification data")
                print(staff_pro_qualification_form.errors)
        else:
            staff_qualification_form = fm.StaffQualificationForm()
            staff_pro_qualification_form = fm.StaffProQualificationForm()
        context = {
            "staff_qualification_form": staff_qualification_form,
            "staff_qualification_list": md.StaffQualification.objects.all(),
            "staff_pro_qualification_form": staff_pro_qualification_form,
            "staff_pro_qualification_list": md.StaffProQualification.objects.all().order_by(
                "StaffProQualificationName"),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_staff_qualification.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddStaffQualification")


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


def add_extras(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            marital_status_form = fm.MaritalStatusForm(request.POST)
            if marital_status_form.is_valid():
                md.MaritalStatus(MaritalStatusID=uuid.uuid4(),
                                 MaritalStatus=marital_status_form.cleaned_data['MaritalStatus'].capitalize()).save()
                return redirect("/Settings/AddExtras")
            else:
                print("Something went wrong while adding the extra data")
        else:
            marital_status_form = fm.MaritalStatusForm()
        context = {
            "marital_status_form": marital_status_form,
            "marital_status_list": md.MaritalStatus.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_extras.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddExtras")


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
                            'ClassLevelName'], ClassLevelCode = class_level_form.cleaned_data[
                            'ClassLevelCode'].upper()).save()
                        return redirect("/Settings/CreateClass")
                else:
                    print(class_level_form.errors)
            elif request.POST.get("form-type") == "class-list-form":
                if class_list_form.is_valid():
                    if not md.ClassList.objects.filter(ClassName = class_list_form.cleaned_data['ClassName'].upper()).exists() and not md.ClassList.objects.filter(OrderID = class_list_form.cleaned_data['OrderID']).exists():
                        md.ClassList(ClassID=uuid.uuid4(), ClassName=class_list_form.cleaned_data['ClassName'].upper(), OrderID = class_list_form.cleaned_data['OrderID']).save()
                        return redirect("/Settings/CreateClass")
                    else:
                        messages.error(request, "Class Name already present")
            elif request.POST.get('form-type') == "section-form":
                if section_form.is_valid():
                    if not md.Section.objects.filter(SectionName = section_form.cleaned_data['SectionName'].upper()).exists():
                        md.Section(SectionID=uuid.uuid4(),
                                   SectionName=section_form.cleaned_data['SectionName'].upper()).save()
                        return redirect("/Settings/CreateClass")
                    else:
                        messages.error(request, "Section already present")
        else:
            class_list = md.ClassList.objects.all().order_by('OrderID')
            new_order_id = class_list.last().OrderID + 1
            class_list_form = fm.ClassListForm(
                initial={'OrderID': new_order_id}
            )
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
        return render(request, "dshiksha_erp/Pages/Settings/add_class.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreateClass")


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


def add_designation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            designation_form = fm.DesignationForm(request.POST)
            staff_subject_form = fm.StaffSubjectForm(request.POST)
            if request.POST.get('form-type') == "designation-form":
                if designation_form.is_valid():
                    md.Designation(DesignationID=uuid.uuid4(),
                                   DesignationName=designation_form.cleaned_data['DesignationName'].capitalize()).save()
                    return redirect("/Settings/AddDesignation")
            elif request.POST.get('form-type') == 'staff-subject-form':
                if staff_subject_form.is_valid():
                    md.StaffSubject(StaffSubjectID=uuid.uuid4(), StaffSubjectName=staff_subject_form.cleaned_data[
                        'StaffSubjectName'].capitalize()).save()
                    return redirect("/Settings/AddDesignation")
        else:
            designation_form = fm.DesignationForm()
            staff_subject_form = fm.StaffSubjectForm()
        context = {
            "designation_form": designation_form,
            "designation_list": md.Designation.objects.all(),
            "staff_subject_form": staff_subject_form,
            "staff_subject_list": md.StaffSubject.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_designation.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddDesignation")


def add_mode_of_transport(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            mot_form = fm.ModeOfTransportForm(request.POST)
            if mot_form.is_valid():
                if md.ModeOfTransport.objects.filter(TransportName=mot_form.cleaned_data['TransportName']).exists():
                    messages.error(request, "Mode of Transport already exists")
                elif md.ModeOfTransport.objects.filter(OrderID=mot_form.cleaned_data['OrderID']).exists():
                    messages.error(request, "Order ID already exists")
                else:
                    md.ModeOfTransport(ModeOfTransportID=uuid.uuid4(),
                                       TransportName=mot_form.cleaned_data['TransportName'].capitalize(),
                                       OrderID=mot_form.cleaned_data['OrderID']).save()
                    return redirect("/Settings/AddModeOfTransport")
            else:
                print(mot_form.errors)
        else:
            mot_form = fm.ModeOfTransportForm()
        context = {
            "mot_form": mot_form,
            "mot_list": md.ModeOfTransport.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_mode_of_transport.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddModeOfTransport")


def add_medium_of_instruction(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            moi_form = fm.MediumOfInstructionForm(request.POST)
            if moi_form.is_valid():
                if md.MediumOfInstruction.objects.filter(
                        MediumOfInstruction=moi_form.cleaned_data['MediumOfInstruction']).exists():
                    messages.error(request, "Medium of Instruction already exists")
                else:
                    md.MediumOfInstruction(MediumOfInstructionID=uuid.uuid4(),
                                           MediumOfInstruction=moi_form.cleaned_data[
                                               'MediumOfInstruction'].capitalize()).save()
                    return redirect("/Settings/AddMediumOfInstruction")
            else:
                print(moi_form.errors)
        else:
            moi_form = fm.MediumOfInstructionForm()
        context = {
            "moi_form": moi_form,
            "moi_list": md.MediumOfInstruction.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_medium_of_instruction.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddMediumOfInstruction")


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
                    return redirect("/Settings/AddSchoolAffiliation")
            else:
                print(sa_form.errors)
        else:
            sa_form = fm.SchoolAffiliationForm()
        context = {
            "sa_form": sa_form,
            "sa_list": md.SchoolAffiliation.objects.all()
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_school_affiliation.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddSchoolAffiliation")


def add_nature_of_appointment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            noa_form = fm.NatureOfAppointmentForm(request.POST)
            if noa_form.is_valid():
                if md.NatureOfAppointment.objects.filter(
                        NatureOfAppointment=noa_form.cleaned_data['NatureOfAppointment']).exists():
                    messages.error(request, "Nature of Appointment already exists")
                else:
                    md.NatureOfAppointment(NatureOfAppointmentID = uuid.uuid4(), NatureOfAppointment = noa_form.cleaned_data['NatureOfAppointment']).save()
                    return redirect("/Settings/AddNatureOfAppointment")
            else:
                print(noa_form.errors)
        else:
            noa_form = fm.NatureOfAppointmentForm()
        context = {
            "noa_form": noa_form,
            "noa_list": md.NatureOfAppointment.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_nature_of_appointment.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddNatureOfAppointment")



def create_school_type(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            st_form = fm.SchoolTypeForm(request.POST)
            if st_form.is_valid():
                if md.SchoolType.objects.filter(SchoolType=st_form.cleaned_data['SchoolType']).exists():
                    messages.error(request, "School Type already exists")
                else:
                    md.SchoolType(SchoolTypeID = uuid.uuid4(), SchoolType = st_form.cleaned_data['SchoolType']).save()
                    return redirect("/Settings/CreateSchoolType")
            else:
                print(st_form.errors)
        else:
            st_form = fm.SchoolTypeForm()
        context = {
            "st_form": st_form,
            "st_list": md.SchoolType.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/create_school_type.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreateSchoolType")


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


def create_institution_level(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            il_form = fm.InstitutionLevelForm(request.POST)
            if il_form.is_valid():
                if md.InstitutionLevel.objects.filter(InstitutionLevel = il_form.cleaned_data['InstitutionLevel']).exists():
                    messages.error(request, "Institution Level already exists")
                else:
                    md.InstitutionLevel(InstitutionLevelID = uuid.uuid4(), InstitutionLevel = il_form.cleaned_data['InstitutionLevel']).save()
                    return redirect("/Settings/CreateInstitutionLevel")
            else:
                print(il_form.errors)
        else:
            il_form = fm.InstitutionLevelForm()
        context = {
            "il_form": il_form,
            "il_list": md.InstitutionLevel.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/create_institution_level.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreateInstitutionLevel")


def create_syllabus_type(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            st_form = fm.SyllabusTypeForm(request.POST)
            if st_form.is_valid():
                if md.SyllabusType.objects.filter(SyllabusType = st_form.cleaned_data['SyllabusType']).exists():
                    messages.error(request, "Syllabus Type already exists")
                else:
                    md.SyllabusType(SyllabusTypeID = uuid.uuid4(), SyllabusType = st_form.cleaned_data['SyllabusType']).save()
                    return redirect("/Settings/CreateSyllabusType")
            else:
                print(st_form.errors)
        else:
            st_form = fm.SyllabusTypeForm()
        context = {
            "st_form": st_form,
            "st_list": md.SyllabusType.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/create_syllabus_type.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreateSyllabusType")


def create_payment_mode(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pt_form = fm.ModeOfPaymentForm(request.POST)
            ps_form = fm.PaymentStatus(request.POST)
            if request.POST.get('form-type') == 'payment-mode':
                if pt_form.is_valid():
                    if md.ModeOfPayment.objects.filter(ModeOfPayment = pt_form.cleaned_data['ModeOfPayment']).exists() or md.ModeOfPayment.objects.filter(OrderID = pt_form.cleaned_data['OrderID']).exists():
                        messages.error(request, "Payment Mode already exists")
                    else:
                        md.ModeOfPayment(ModeOfPaymentID = uuid.uuid4(), ModeOfPayment = pt_form.cleaned_data['ModeOfPayment'], OrderID = pt_form.cleaned_data['OrderID']).save()
                        return redirect("/Settings/CreatePaymentMode")
                else:
                    print(pt_form.errors)
            elif request.POST.get('form-type') == 'payment-status':
                if ps_form.is_valid():
                    if md.PaymentStatus.objects.filter(PaymentStatus = ps_form.cleaned_data['PaymentStatus']).exists():
                        messages.error(request, "Payment Status already exists")
                    else:
                        md.PaymentStatus(PaymentStatusID = uuid.uuid4(), PaymentStatus = ps_form.cleaned_data['PaymentStatus']).save()
                        return redirect("/Settings/CreatePaymentMode")
                else:
                    print(ps_form.errors)
        else:
            print(md.ModeOfPayment.objects.all().last())
            if md.ModeOfPayment.objects.all().last() is None:
                order_id = 1
            else:
                order_id = md.ModeOfPayment.objects.all().last().OrderID + 1
            pt_form = fm.ModeOfPaymentForm(initial = {"OrderID": order_id})
            ps_form = fm.PaymentStatus()
        context = {
            "pt_form": pt_form,
            "pt_list": md.ModeOfPayment.objects.all().order_by('OrderID'),
            "ps_form": ps_form,
            "ps_list": md.PaymentStatus.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/create_payment_mode.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreatePaymentMode")


def create_correspondent(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cr_form = fm.CorrespondentForm(request.POST)
            if cr_form.is_valid():
                if User.objects.filter(Email = cr_form.cleaned_data['CorrespondentEmail']).exists():
                    messages.error("Correspondent Already present")
                else:
                    user = User.objects.create_user(
                        email = cr_form.cleaned_data['CorrespondentEmail'],
                        first_name = cr_form.cleaned_data['CorrespondentFirstName'],
                        username = cr_form.cleaned_data['Username'],
                        password = cr_form.cleaned_data['Password'],
                        UserType=UserTypes.objects.get(UserTypeName="Correspondent").UserTypeID
                    )
                    md.Correspondent(
                        CorrespondentID = uuid.uuid4(), CorrespondentFirstName = cr_form.cleaned_data['CorrespondentFirstName'], CorrespondentLastName = cr_form.cleaned_data['CorrespondentLastName'], CorrespondentEmail = cr_form.cleaned_data['CorrespondentEmail'], CorrespondentMobile = cr_form.cleaned_data['CorrespondentMobile'], CorrespondentWhatsAppNo = cr_form.cleaned_data['CorrespondentWhatsAppNo'], UserID = User.objects.get(UserID = user.UserID)
                    ).save()
                    return redirect("/Settings/CreateCorrespondent")
            else:
                print(cr_form.errors)
        else:
            cr_form = fm.CorrespondentForm()
        context = {
            "cr_form": cr_form,
            "cr_list": md.Correspondent.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/create_correspondent.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreateCorrespondent")


def create_fees_type(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ft_form = fm.FeesTypeForm(request.POST)
            installment_form = fm.InstallmentForm(request.POST)

            if request.POST.get('form-type') == "fees-type-form":
                if ft_form.is_valid():
                    if not md.FeesType.objects.filter(FeesTypeName = ft_form.cleaned_data['FeesTypeName']).exists() and not md.FeesType.objects.filter(FeeTypeCode = ft_form.cleaned_data['FeeTypeCode']).exists():
                        md.FeesType(FeesTypeID = uuid.uuid4(), FeesTypeName = ft_form.cleaned_data['FeesTypeName'], FeeTypeCode = ft_form.cleaned_data['FeeTypeCode']).save()
                        return redirect("/Settings/CreateFeesType")
                    else:
                        print("Something went wrong")
                        messages.error(request, "Fees Type already exists")
                else:
                    print(ft_form.errors)
            elif request.POST.get("form-type") == "installment-form":
                if installment_form.is_valid():
                    if not md.Installment.objects.filter(InstallmentName = installment_form.cleaned_data['InstallmentName']).exists():
                        md.Installment(InstallmentID = uuid.uuid4(), InstallmentName = installment_form.cleaned_data['InstallmentName']).save()
                        return redirect("/Settings/CreateFeesType")
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
        return render(request, "dshiksha_erp/Pages/Settings/create_fees_type.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/create_fees_type")


def create_sub_fee_type(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sft_form = fm.SubFeeForm(request.POST)
            if sft_form.is_valid():
                if sft_form.cleaned_data['FeesType'] is not None:
                    for i in range(1, int(request.POST.get('FeesTypeCount')) + 1):
                        print(request.POST.get('subfee-type-'+str(i)))
                        if md.SubFee.objects.filter(SubFeeName = request.POST.get('subfee-type-'+str(i)), FeesType = sft_form.cleaned_data['FeesType']).exists():
                            messages.error(request, "Sub Fee Type already exists")
                        else:
                            md.SubFee(SubFeeID = uuid.uuid4(), SubFeeName = request.POST.get('subfee-type-'+str(i)), FeesType = sft_form.cleaned_data['FeesType']).save()
                    return redirect("/Settings/CreateSubFeesType")
                else:
                    messages.error(request, "Fees Type is required")
            else:
                print(sft_form.errors)
        else:
            sft_form = fm.SubFeeForm()
        context = {
            "sft_form": sft_form,
            "sft_list": md.SubFee.objects.all().order_by('SubFeeName'),
            "fs_list": md.FeesType.objects.all().order_by('FeesTypeName'),
            "fees_type_count": 1,
        }
        return render(request, "dshiksha_erp/Pages/Settings/create_sub_fee_type.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/CreateSubFeesType")

def add_class_level_fees(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            clf_form = fm.ClassLevelFeesForm(request.POST)
            if clf_form.is_valid():
                if md.ClassLevelFees.objects.filter(ClassLevel = clf_form.cleaned_data['ClassLevel'], FeesType = clf_form.cleaned_data['FeesType']).exists() and md.ClassLevelFees.objects.filter(FeesType = clf_form.cleaned_data['FeesType']).exists():
                    messages.error(request, "Class Level Fees Already Present")
                else:
                    md.ClassLevelFees(ClassLevelFeesID = uuid.uuid4(), ClassLevel = clf_form.cleaned_data['ClassLevel'], FeesType = clf_form.cleaned_data['FeesType']).save()
                    return redirect("/Settings/ClassLevelFees")
            else:
                print(clf_form.errors)
        else:
            clf_form = fm.ClassLevelFeesForm()
        context = {
                    "clf_form": clf_form,
                    "class_list": md.ClassLevel.objects.all().order_by("ClassLevelName"),
                    "fees_type_list": md.FeesType.objects.all().order_by("FeesTypeName"),
                    "class_level_fees_list": md.ClassLevelFees.objects.all().order_by("ClassLevel__ClassLevelName", "FeesType__FeesTypeName"),
                }

        return render(request, "dshiksha_erp/Pages/Settings/add_class_level_fees.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/ClassLevelFees")


# views related to CBSE
def cbse_assign_class_level(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            class_form = fm.ClassForm(request.POST)
            if class_form.is_valid():
                if cbm.Class.objects.filter(ClassList = class_form.cleaned_data['ClassList'], ClassLevel = class_form.cleaned_data['ClassLevel']).exists():
                    messages.error(request, "Class already assigned")
                else:
                    cbm.Class(ClassID=uuid.uuid4(), ClassList=class_form.cleaned_data['ClassList'],
                             ClassLevel=class_form.cleaned_data['ClassLevel']).save()
                    return redirect("/CBSE/AssignClassLevel")
            else:
                print("Something went wrong")
                print(class_form.errors)
        else:
            class_form = fm.ClassForm()
        context = {
            "class_form": class_form,
            "class_list": cbm.Class.objects.all().order_by('ClassList__OrderID',),
            "classes_list": md.ClassList.objects.all().order_by('OrderID'),
            "class_level_list": md.ClassLevel.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/CBSE/assign_class_level.html", context)
    else:
        return redirect("/accounts/login/>redirect_to=/CBSE/AssignClassLevel")


def create_cbse_school(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cbse_school_form = fm.SchoolForm(request.POST)
            if cbse_school_form.is_valid():
                if cbm.School.objects.filter(SchoolName=cbse_school_form.cleaned_data['SchoolName'],
                                             Email=cbse_school_form.cleaned_data['Email']).exists():
                    messages.error(request, "School Already Present")
                elif cbm.School.objects.filter(SchoolName=cbse_school_form.cleaned_data['SchoolName']).exists():
                    messages.error(request, "School Name already present")
                elif cbm.School.objects.filter(Email=cbse_school_form.cleaned_data['Email']).exists():
                    messages.error(request, "School Email already present")
                elif cbm.School.objects.filter(SchoolCode=cbse_school_form.cleaned_data['SchoolCode']).exists():
                    messages.error(request, "School Code already present")
                elif cbm.School.objects.filter(SchoolUsername=cbse_school_form.cleaned_data['SchoolUsername']).exists():
                    messages.error(request, "School Username already present")
                else:
                    user = User.objects.create_user(email=cbse_school_form.cleaned_data['Email'],
                                                    first_name=cbse_school_form.cleaned_data['SchoolName'],
                                                    username=cbse_school_form.cleaned_data['SchoolCode'],
                                                    password=cbse_school_form.cleaned_data['Password'],
                                                    UserType=UserTypes.objects.get(UserTypeName="CBSE").UserTypeID)
                    school_data = cbm.School(SchoolID=uuid.uuid4(),
                                             SchoolName=cbse_school_form.cleaned_data['SchoolName'].capitalize(),
                                             SchoolType="CBSE", Email=cbse_school_form.cleaned_data['Email'],
                                             Village=cbse_school_form.cleaned_data['Village'],
                                             Pincode=cbse_school_form.cleaned_data['Pincode'],
                                             Parish=cbse_school_form.cleaned_data['Parish'],
                                             UserID=User.objects.get(UserID=user.UserID),
                                             SchoolUsername=cbse_school_form.cleaned_data['SchoolUsername'],
                                             SchoolCode=cbse_school_form.cleaned_data['SchoolCode'],
                                             CurrentAcademicYear = cbse_school_form.cleaned_data['CurrentAcademicYear'], # Add academic Year support in web page
                                             Landline=cbse_school_form.cleaned_data['Landline'])
                    school_data.save()
                    redirect("/CBSE/create_school")
            else:
                print(cbse_school_form.errors)
        else:
            cbse_school_form = fm.SchoolForm()
        context = {
            "school_form": cbse_school_form,
            "village_list": md.Village.objects.all(),
            "parish_list": md.Parish.objects.all(),
            "post_office_list": md.PostOffice.objects.all(),
            "school_list": cbm.School.objects.all(),
            "academic_year_list": md.AcademicYear.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/CBSE/create_cbse_school.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/CBSE/create_school")
