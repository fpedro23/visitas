# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('visitas_stg', '0010_auto_20151019_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='capitalizacion',
            name='nombre_medio',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Nombre De Medio', blank=True),
            preserve_default=True,
        ),
    ]
