# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20170803_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]