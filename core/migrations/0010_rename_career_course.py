# Generated by Django 4.2.7 on 2023-12-13 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_application_approved_by_application_disapproved_by_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Career',
            new_name='Course',
        ),
    ]
