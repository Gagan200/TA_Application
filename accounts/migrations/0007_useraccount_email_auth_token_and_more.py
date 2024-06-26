# Generated by Django 4.2.7 on 2024-03-06 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_useraccount_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='email_auth_token',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='verified_email',
            field=models.BooleanField(default=False),
        ),
    ]
