# Generated by Django 3.1.5 on 2021-01-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asvstool', '0003_auto_20210124_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(default=None, max_length=256, unique=True),
        ),
    ]
