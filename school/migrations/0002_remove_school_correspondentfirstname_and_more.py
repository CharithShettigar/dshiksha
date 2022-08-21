# Generated by Django 4.0.4 on 2022-08-21 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='CorrespondentFirstName',
        ),
        migrations.RemoveField(
            model_name='school',
            name='CorrespondentLastName',
        ),
        migrations.AddField(
            model_name='school',
            name='CorrespondentName',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='students',
            name='FatherEmail',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='FatherIncome',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='FatherMobileNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='FatherName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='FatherOccupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='FatherQualification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='FatherWhatsappNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='GaurdianEmail',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='GaurdianIncome',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='GaurdianMobileNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='GaurdianName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='GaurdianOccupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='GaurdianQualification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='GaurdianWhatsappNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='MotherEmail',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='MotherIncome',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='MotherMobileNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='MotherName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='MotherOccupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='MotherQualification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='MotherWhatsappNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]
