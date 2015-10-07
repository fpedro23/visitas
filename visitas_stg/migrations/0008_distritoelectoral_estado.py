# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitas_stg', '0007_auto_20151007_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='distritoelectoral',
            name='estado',
            field=models.ForeignKey(default=1, to='visitas_stg.Estado'),
            preserve_default=True,
        ),
    ]
