# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-19 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_seguridad', '0017_persona_enviar_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerta',
            name='usuario',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='alerta',
            name='vehiculo',
            field=models.CharField(max_length=25),
        ),
    ]
