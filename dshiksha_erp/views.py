from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from main.models import User, UserTypes
import dshiksha_erp.forms as fm
from django.contrib import messages
import dshiksha_erp.models as md
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
        # return render(request, 'dshiksha_erp/Pages/dashboard.html')
    else:
        return redirect("/")



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


def add_subject(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            staff_subject_form = fm.StaffSubjectForm(request.POST)
            if request.POST.get('form-type') == 'staff-subject-form':
                if staff_subject_form.is_valid():
                    md.StaffSubject(StaffSubjectID=uuid.uuid4(), StaffSubjectName=staff_subject_form.cleaned_data[
                        'StaffSubjectName'].capitalize()).save()
                    return redirect("/Settings/AddSubject")
        else:
            staff_subject_form = fm.StaffSubjectForm()
        context = {
            "staff_subject_form": staff_subject_form,
            "staff_subject_list": md.StaffSubject.objects.all(),
        }
        return render(request, "dshiksha_erp/Pages/Settings/add_subject.html", context)
    else:
        return redirect("/accounts/login/?redirect_to=/Settings/AddSubject")

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