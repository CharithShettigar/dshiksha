# Generated by Django 4.0.4 on 2022-08-07 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dshiksha_erp', '0002_bank_online'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('ApplicationID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('ApplicationNo', models.CharField(max_length=100)),
                ('StudentName', models.CharField(max_length=100)),
                ('StudentDOB', models.DateField()),
                ('StudentMobileNo', models.CharField(max_length=30)),
                ('ParentName', models.CharField(max_length=100)),
                ('ParentMobileNo', models.CharField(max_length=30)),
                ('ApplicationDate', models.DateField()),
                ('Amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AssignClass',
            fields=[
                ('AssignClassID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('AcademicYear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.academicyear')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('ClassID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ClassLevel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.classlevel')),
                ('ClassList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.classlist')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('SchoolID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('SchoolName', models.CharField(max_length=100)),
                ('SchoolLogo', models.CharField(max_length=250)),
                ('SchoolDISECode', models.CharField(max_length=100)),
                ('SchoolType', models.CharField(max_length=100)),
                ('Landline', models.CharField(max_length=100)),
                ('Mobile', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=100)),
                ('Website', models.CharField(max_length=100)),
                ('EstDate', models.DateField(null=True)),
                ('History', models.TextField(max_length=5000)),
                ('SchoolPANNo', models.CharField(max_length=100)),
                ('GSTINo', models.CharField(max_length=100)),
                ('SchoolCode', models.CharField(max_length=25)),
                ('SchoolUsername', models.CharField(max_length=50)),
                ('SyllabusType', models.CharField(max_length=100)),
                ('AccountantName', models.CharField(max_length=100)),
                ('AccountantEmail', models.EmailField(max_length=100)),
                ('AccountantMobile', models.CharField(max_length=100)),
                ('AccountantWhatsAppNo', models.CharField(max_length=100)),
                ('CorrespondentFirstName', models.CharField(max_length=100)),
                ('CorrespondentLastName', models.CharField(max_length=100, null=True)),
                ('CorrespondentEmail', models.EmailField(max_length=100)),
                ('CorrespondentMobile', models.CharField(max_length=100)),
                ('CorrespondentWhatsAppNo', models.CharField(max_length=100)),
                ('Area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.area')),
                ('CurrentAcademicYear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.academicyear')),
                ('InsitutionLevel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.institutionlevel')),
                ('Pincode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.postoffice')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Village', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.village')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('SubjectID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('SubjectName', models.CharField(max_length=50)),
                ('AssignClass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.assignclass')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('AdmissionID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('AdmissionNo', models.CharField(max_length=100)),
                ('AdmissionDate', models.DateField()),
                ('PreviousSchoolName', models.CharField(max_length=100)),
                ('StudentName', models.CharField(max_length=100)),
                ('StudentDOB', models.DateField()),
                ('StudentMobileNo', models.CharField(max_length=30)),
                ('StudentPhoto', models.CharField(max_length=100)),
                ('AddressLine1', models.CharField(max_length=100)),
                ('AddressLine2', models.CharField(max_length=100)),
                ('FatherName', models.CharField(max_length=100)),
                ('FatherMobileNo', models.CharField(max_length=100)),
                ('FatherWhatsappNo', models.CharField(max_length=100)),
                ('FatherEmail', models.EmailField(max_length=100)),
                ('FatherQualification', models.CharField(max_length=100)),
                ('FatherOccupation', models.CharField(max_length=100)),
                ('FatherIncome', models.FloatField(null=True)),
                ('MotherName', models.CharField(max_length=100)),
                ('MotherMobileNo', models.CharField(max_length=100)),
                ('MotherWhatsappNo', models.CharField(max_length=100)),
                ('MotherEmail', models.EmailField(max_length=100)),
                ('MotherQualification', models.CharField(max_length=100)),
                ('MotherOccupation', models.CharField(max_length=100)),
                ('MotherIncome', models.FloatField(null=True)),
                ('GaurdianName', models.CharField(max_length=100)),
                ('GaurdianMobileNo', models.CharField(max_length=100)),
                ('GaurdianWhatsappNo', models.CharField(max_length=100)),
                ('GaurdianEmail', models.EmailField(max_length=100)),
                ('GaurdianQualification', models.CharField(max_length=100)),
                ('GaurdianOccupation', models.CharField(max_length=100)),
                ('GaurdianIncome', models.FloatField(null=True)),
                ('Application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.application')),
                ('BloodGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.bloodgroup')),
                ('Caste', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.caste')),
                ('CasteCategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.castecategory')),
                ('Class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class')),
                ('Gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.gender')),
                ('MotherTongue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.mothertongue')),
                ('Nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.nationality')),
                ('Pincode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.postoffice')),
                ('Religion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.religion')),
                ('SchoolID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
                ('Village', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.village')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('StaffID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('StaffName', models.CharField(max_length=100)),
                ('StaffEmailID', models.EmailField(max_length=100)),
                ('StaffMobile', models.CharField(max_length=10)),
                ('StaffPhoto', models.CharField(max_length=250)),
                ('DOB', models.DateField(null=True)),
                ('AddressLine1', models.CharField(max_length=100)),
                ('AddressLine2', models.CharField(max_length=100)),
                ('StaffWhatsAppNo', models.CharField(max_length=25)),
                ('DateOfAppointment', models.DateField(null=True)),
                ('DateOfRetirement', models.DateField(null=True)),
                ('StaffNo', models.CharField(max_length=50)),
                ('AcademicYear', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.academicyear')),
                ('BloodGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.bloodgroup')),
                ('Caste', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.caste')),
                ('Designation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.designation')),
                ('Gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.gender')),
                ('MaritalStatus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.maritalstatus')),
                ('MotherTongue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.mothertongue')),
                ('Pincode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.postoffice')),
                ('SchoolID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
                ('StaffQualification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.staffqualification')),
                ('Subject1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Subject1', to='dshiksha_erp.staffsubject')),
                ('Subject2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Subject2', to='dshiksha_erp.staffsubject')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Village', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.village')),
            ],
        ),
        migrations.CreateModel(
            name='SCHOOLHead',
            fields=[
                ('SCHOOLHeadID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('School', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
                ('Staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('ChapterID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ChapterName', models.CharField(max_length=50)),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
            ],
        ),
        migrations.AddField(
            model_name='assignclass',
            name='Class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class'),
        ),
        migrations.AddField(
            model_name='assignclass',
            name='School',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school'),
        ),
        migrations.AddField(
            model_name='assignclass',
            name='Section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.section'),
        ),
        migrations.CreateModel(
            name='ApplicationNo',
            fields=[
                ('ApplicationNoID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('Amount', models.FloatField()),
                ('ApplicationNo', models.IntegerField()),
                ('AcademicYear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.academicyear')),
                ('Class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class')),
                ('School', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='Class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class'),
        ),
        migrations.AddField(
            model_name='application',
            name='Gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.gender'),
        ),
        migrations.AddField(
            model_name='application',
            name='ModeOfPayment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.modeofpayment'),
        ),
        migrations.AddField(
            model_name='application',
            name='SchoolID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school'),
        ),
    ]
