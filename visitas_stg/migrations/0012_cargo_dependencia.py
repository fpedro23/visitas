# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('visitas_stg', '0011_capitalizacion_nombre_medio'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='dependencia',
            field=models.ForeignKey(blank=True, to='visitas_stg.Dependencia', null=True),
            preserve_default=True,
        ),
    ]
