# Generated by Django 4.0.4 on 2022-08-13 10:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_students_application'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendances',
            fields=[
                ('AttendanceID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('AttendanceDate', models.DateField()),
                ('AttendanceMark', models.CharField(max_length=100)),
                ('AssignClass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.assignclass')),
                ('SchoolID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
                ('StudentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.students')),
            ],
        ),
    ]
