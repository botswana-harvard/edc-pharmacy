# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_pharma', '0011_auto_20171019_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='slug',
            field=models.CharField(db_index=True, default='', editable=False, help_text='a field used for quick search', max_length=250, null=True),
        ),
    ]
