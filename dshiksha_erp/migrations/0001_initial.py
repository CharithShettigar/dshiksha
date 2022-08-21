# Generated by Django 4.0.4 on 2022-08-19 15:16

from django.db import migrations, models
import django.db.models.deletion
import dshiksha_erp.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('AcademicYearID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('AcademicYear', models.CharField(max_length=50)),
                ('IsActive', models.BooleanField()),
                ('OrderID', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('AreaID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('AreaType', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('BankID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('BankName', models.CharField(max_length=50)),
                ('OrderID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BloodGroup',
            fields=[
                ('BloodGroupID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('BloodGroupName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CasteCategory',
            fields=[
                ('CasteCategoryID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('CasteCategoryName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClassLevel',
            fields=[
                ('ClassLevelID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('ClassLevelName', models.CharField(max_length=50)),
                ('ClassLevelCode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('ClassID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('ClassName', models.CharField(max_length=50)),
                ('OrderID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('DesignationID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('DesignationName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('DistrictID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('DistrictName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('FeedbackID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('FeedbackData', models.TextField(max_length=500, null=True)),
                ('FeedbackFile', models.FileField(null=True, upload_to=dshiksha_erp.models.filepath_feedback)),
                ('School', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FeesType',
            fields=[
                ('FeesTypeID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('FeesTypeName', models.CharField(max_length=50)),
                ('FeeTypeCode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('GenderID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('GenderName', models.CharField(max_length=50)),
                ('GenderOrder', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('InstallmentID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('InstallmentName', models.CharField(max_length=50)),
                ('OrderID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionLevel',
            fields=[
                ('InstitutionLevelID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('InstitutionLevel', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('MaritalStatusID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('MaritalStatus', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ModeOfPayment',
            fields=[
                ('ModeOfPaymentID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ModeOfPayment', models.CharField(max_length=50)),
                ('OrderID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ModeOfTransport',
            fields=[
                ('ModeOfTransportID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('TransportName', models.CharField(max_length=50)),
                ('OrderID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MotherTongue',
            fields=[
                ('MotherTongueID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('MotherTongueName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('NationalityID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('NationalityName', models.CharField(max_length=50)),
                ('CountryCode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NatureOfAppointment',
            fields=[
                ('NatureOfAppointmentID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('NatureOfAppointment', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Online',
            fields=[
                ('OnlineID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('OnlineAppName', models.CharField(max_length=50)),
                ('OrderID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentStatus',
            fields=[
                ('PaymentStatusID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('PaymentStatus', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PostOffice',
            fields=[
                ('PostOfficeID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('PostOfficeName', models.CharField(max_length=50)),
                ('Pincode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('ReligionID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ReligionName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolAffiliation',
            fields=[
                ('SchoolAffiliationID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('SchoolAffiliation', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolType',
            fields=[
                ('SchoolTypeID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('SchoolType', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('SectionID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('SectionName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StaffQualification',
            fields=[
                ('StaffQualificationID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('StaffQualificationName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StaffSubject',
            fields=[
                ('StaffSubjectID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('StaffSubjectName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('StateID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('StateName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Taluk',
            fields=[
                ('TalukID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('TalukName', models.CharField(max_length=50)),
                ('District', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.district')),
            ],
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('VillageID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('VillageName', models.CharField(max_length=50)),
                ('Taluk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.taluk')),
            ],
        ),
        migrations.CreateModel(
            name='TransportData',
            fields=[
                ('TransportDataID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('DriverName', models.CharField(max_length=50, null=True)),
                ('DriverMobileNo', models.CharField(max_length=50, null=True)),
                ('DriverEmail', models.EmailField(max_length=50, null=True)),
                ('DriverAddress', models.TextField(null=True)),
                ('ModeOfTransport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.modeoftransport')),
            ],
        ),
        migrations.CreateModel(
            name='SubFee',
            fields=[
                ('SubFeeID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('SubFeeName', models.CharField(max_length=50)),
                ('FeesType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.feestype')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='State',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.state'),
        ),
        migrations.CreateModel(
            name='ClassLevelFees',
            fields=[
                ('ClassLevelFeesID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('ClassLevel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.classlevel')),
                ('FeesType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.feestype')),
            ],
        ),
        migrations.CreateModel(
            name='Caste',
            fields=[
                ('CasteID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('CasteName', models.CharField(max_length=50)),
                ('CasteCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.castecategory')),
                ('Religion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dshiksha_erp.religion')),
            ],
        ),
    ]
