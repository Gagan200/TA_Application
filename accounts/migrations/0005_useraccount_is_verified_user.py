# Generated by Django 4.2.7 on 2023-12-12 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_useraccount_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_verified_user',
            field=models.BooleanField(default=False),
        ),
    ]
