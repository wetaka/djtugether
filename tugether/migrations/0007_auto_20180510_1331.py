# Generated by Django 2.0.4 on 2018-05-10 06:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tugether', '0006_auto_20180510_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='limited',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10000)]),
        ),
    ]
