# Generated by Django 4.0.4 on 2022-08-12 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='AssignClass',
        ),
        migrations.AddField(
            model_name='students',
            name='AssignedClass',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.assignclass'),
        ),
    ]
