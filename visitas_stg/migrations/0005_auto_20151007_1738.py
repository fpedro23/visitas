# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitas_stg', '0004_auto_20151006_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='clasificacion',
            field=models.ForeignKey(verbose_name=b'Clasificaci\xc3\xb3n', to='visitas_stg.Clasificacion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='descripcion',
            field=models.CharField(max_length=200, verbose_name=b'Descripci\xc3\xb3n'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='tipo_actividad',
            field=models.ForeignKey(verbose_name=b'Tipo de Actividad', to='visitas_stg.TipoActividad'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participantelocal',
            name='cargo',
            field=models.CharField(max_length=200, verbose_name=b'Cargo del participante local'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participantelocal',
            name='nombre',
            field=models.CharField(max_length=200, verbose_name=b'Nombre de participante local'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='cargo',
            field=models.ForeignKey(verbose_name=b'Cargo que ejecuta', to='visitas_stg.Cargo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='dependencia',
            field=models.ForeignKey(default=1, verbose_name=b'Dependencia', to='visitas_stg.Dependencia'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='distrito_electoral',
            field=models.IntegerField(default=0, verbose_name=b'Distrito electoral'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='entidad',
            field=models.ForeignKey(verbose_name=b'Entidad', to='visitas_stg.Estado'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='fecha_visita',
            field=models.DateField(verbose_name=b'Fecha de Visita'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='municipio',
            field=models.ForeignKey(verbose_name=b'Municipio', to='visitas_stg.Municipio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='partido_gobernante',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Partido Gobernante', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visita',
            name='region',
            field=models.ForeignKey(verbose_name=b'Regi\xc3\xb3n', to='visitas_stg.Region'),
            preserve_default=True,
        ),
    ]
