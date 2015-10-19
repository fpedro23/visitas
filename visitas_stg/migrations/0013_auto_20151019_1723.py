# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('visitas_stg', '0012_cargo_dependencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='dependencia',
            field=models.ForeignKey(default=1, to='visitas_stg.Dependencia'),
            preserve_default=True,
        ),
    ]
