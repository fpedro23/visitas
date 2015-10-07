# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitas_stg', '0005_auto_20151007_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistritoElectoral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_distrito_electoral', models.CharField(max_length=200, verbose_name=b'Distrito Electoral')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='CargoLocal',
        ),
        migrations.AddField(
            model_name='municipio',
            name='distrito_electoral',
            field=models.ForeignKey(default=1, to='visitas_stg.DistritoElectoral'),
            preserve_default=True,
        ),
    ]
