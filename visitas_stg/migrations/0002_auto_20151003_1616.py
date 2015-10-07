# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('visitas_stg', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='capitalizacion',
            options={'verbose_name': 'Capitalizaci\xf3n', 'verbose_name_plural': 'Capitalizaciones'},
        ),
        migrations.AlterModelOptions(
            name='cargo',
            options={'verbose_name': 'Cargo', 'verbose_name_plural': 'Cargos'},
        ),
        migrations.AlterModelOptions(
            name='cargolocal',
            options={'verbose_name': 'Cargo local', 'verbose_name_plural': 'Cargos locales'},
        ),
        migrations.AlterModelOptions(
            name='clasificacion',
            options={'verbose_name': 'Clasificaci\xf3n', 'verbose_name_plural': 'Clasificaciones'},
        ),
        migrations.AlterModelOptions(
            name='dependencia',
            options={'verbose_name': 'Dependencia', 'verbose_name_plural': 'Dependencias'},
        ),
        migrations.AlterModelOptions(
            name='medio',
            options={'verbose_name': 'Medio', 'verbose_name_plural': 'Medios'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Regi\xf3n', 'verbose_name_plural': 'Regiones'},
        ),
        migrations.AlterModelOptions(
            name='tipoactividad',
            options={'verbose_name': 'Tipo de Actividad', 'verbose_name_plural': 'Tipos de Actividad'},
        ),
        migrations.AlterModelOptions(
            name='tipocapitalizacion',
            options={'verbose_name': 'Tipo de Capitalizaci\xf3n', 'verbose_name_plural': 'Tipos de Capitalizaci\xf3n'},
        ),
        migrations.AlterModelOptions(
            name='visita',
            options={'verbose_name': 'Visita', 'verbose_name_plural': 'Visitas'},
        ),
        migrations.AddField(
            model_name='visita',
            name='distrito_electoral',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='visita',
            name='partido_gobernante',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
