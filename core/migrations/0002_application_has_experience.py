# Generated by Django 4.2.7 on 2023-12-01 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='has_experience',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]