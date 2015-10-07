# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitas_stg', '0006_auto_20151007_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visita',
            name='distrito_electoral',
            field=models.ForeignKey(default=0, verbose_name=b'Distrito electoral', to='visitas_stg.DistritoElectoral'),
            preserve_default=True,
        ),
    ]
