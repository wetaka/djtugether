# Generated by Django 2.0.4 on 2018-05-10 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tugether', '0003_noti'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='enddate',
        ),
        migrations.RemoveField(
            model_name='event',
            name='startdate',
        ),
    ]