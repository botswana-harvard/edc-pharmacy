# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 08:07
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edc_pharma', '0002_auto_20161115_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initials', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator('^[A-Z]{2,4}$', message='Use CAPS, 2-4 letters')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]