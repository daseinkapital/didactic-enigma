# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_auto_20170724_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='districts',
            name='zoom',
            field=models.FloatField(),
        ),
    ]
