# Generated by Django 3.1.2 on 2020-10-23 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniboxapi', '0005_groupfilepermission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'permissions': [('can_view', 'Can view file'), ('can_download', 'Can download file')]},
        ),
    ]