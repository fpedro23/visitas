# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('visitas_stg', '0002_auto_20151003_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblematicaSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problematica_social', models.CharField(max_length=200)),
                ('actividad', models.ForeignKey(to='visitas_stg.Actividad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='actividad',
            name='problematica',
        ),
    ]
