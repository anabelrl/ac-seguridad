# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-01 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_seguridad', '0015_auto_20171001_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacionamiento',
            name='monto_tarifa',
            field=models.FloatField(default=1000),
        ),
    ]