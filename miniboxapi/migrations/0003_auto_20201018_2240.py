# Generated by Django 3.1.2 on 2020-10-19 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniboxapi', '0002_auto_20201013_2244'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='file',
            constraint=models.UniqueConstraint(fields=('company', 'name', 'path'), name='unique_trio'),
        ),
    ]
