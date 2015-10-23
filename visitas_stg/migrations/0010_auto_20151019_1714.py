# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('visitas_stg', '0009_visita_identificador_unico'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartidoGobernante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_partido_gobernante', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='visita',
            name='partido_gobernante',
            field=models.ForeignKey(verbose_name=b'Partido Gobernante', blank=True, to='visitas_stg.PartidoGobernante',
                                    null=True),
            preserve_default=True,
        ),
    ]
