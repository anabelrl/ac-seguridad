# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ac_seguridad', '0002_auto_20170808_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiculo',
            old_name='cedula',
            new_name='dueno',
        ),
    ]
