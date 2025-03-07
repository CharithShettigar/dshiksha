# Generated by Django 4.0.4 on 2022-08-19 06:21

from django.db import migrations, models
import dshiksha_erp.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dshiksha_erp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('FeedbackID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('FeedbackData', models.TextField(max_length=500, null=True)),
                ('FeedbackFile', models.FileField(null=True, upload_to=dshiksha_erp.models.filepath_feedback)),
                ('School', models.CharField(max_length=100)),
                ('FeedbackDate', models.DateTimeField(auto_now=True)),
            ],
        )
        
    ]
