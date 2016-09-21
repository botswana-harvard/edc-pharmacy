# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_pharma', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispense',
            name='total_concentration',
            field=models.CharField(blank=True, help_text='Only required if dispense type IV is chosen', max_length=15, null=True),
        ),
    ]