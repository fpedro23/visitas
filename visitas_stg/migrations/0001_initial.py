# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('problematica', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Capitalizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('evidencia_grafica', models.FileField(null=True, upload_to=b'', blank=True)),
                ('actividad', models.ForeignKey(to='visitas_stg.Actividad')),
            ],
            options={
                'verbose_name': 'Capitalizaci\xf3n',
                'verbose_name_plural': 'Capitalizaci\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_cargo', models.CharField(max_length=200)),
                ('nombre_funcionario', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CargoLocal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_cargo', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Clasificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_clasificacion', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreDependencia', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreEstado', models.CharField(max_length=200)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Medio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_medio', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreMunicipio', models.CharField(max_length=200)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('estado', models.ForeignKey(to='visitas_stg.Estado')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipanteLocal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('actividad', models.ForeignKey(to='visitas_stg.Actividad')),
                ('cargo', models.ForeignKey(to='visitas_stg.CargoLocal')),
            ],
            options={
                'verbose_name': 'Participante local',
                'verbose_name_plural': 'Participantes locales',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numeroRegion', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoActividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_actividad', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoCapitalizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_tipo_capitalizacion', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_visita', models.DateField(verbose_name=b'Fecha')),
                ('cargo', models.ForeignKey(to='visitas_stg.Cargo')),
                ('dependencia', models.ForeignKey(default=1, to='visitas_stg.Dependencia')),
                ('entidad', models.ForeignKey(to='visitas_stg.Estado')),
                ('municipio', models.ForeignKey(to='visitas_stg.Municipio')),
                ('region', models.ForeignKey(to='visitas_stg.Region')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='estado',
            name='region',
            field=models.ForeignKey(to='visitas_stg.Region'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='capitalizacion',
            name='medio',
            field=models.ForeignKey(to='visitas_stg.Medio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='capitalizacion',
            name='tipo_capitalizacion',
            field=models.ForeignKey(to='visitas_stg.TipoCapitalizacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actividad',
            name='clasificacion',
            field=models.ForeignKey(to='visitas_stg.Clasificacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actividad',
            name='tipo_actividad',
            field=models.ForeignKey(to='visitas_stg.TipoActividad'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actividad',
            name='visita',
            field=models.ForeignKey(default=1, to='visitas_stg.Visita'),
            preserve_default=True,
        ),
    ]
