# Generated by Django 4.2.7 on 2023-12-01 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(default='2023-2-2'),
            preserve_default=False,
        ),
    ]