# Generated by Django 3.1.5 on 2021-01-28 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asvstool', '0011_auto_20210128_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='nist',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]