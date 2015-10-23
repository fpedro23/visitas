# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('visitas_stg', '0008_distritoelectoral_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='visita',
            name='identificador_unico',
            field=models.SlugField(unique=True, null=True, verbose_name=b'Identificador \xc3\x9anico'),
            preserve_default=True,
        ),
    ]
