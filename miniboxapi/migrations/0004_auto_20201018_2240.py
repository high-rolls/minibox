# Generated by Django 3.1.2 on 2020-10-19 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniboxapi', '0003_auto_20201018_2240'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='file',
            name='unique_trio',
        ),
        migrations.AddConstraint(
            model_name='file',
            constraint=models.UniqueConstraint(fields=('company', 'name', 'path'), name='file_unique_trio'),
        ),
    ]
