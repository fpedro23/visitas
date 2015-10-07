# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visitas_stg', '0003_auto_20151003_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rol', models.CharField(default=b'US', max_length=2, choices=[(b'AD', b'Administrador general'),
                                                                               (b'US', b'Usuario de Dependencia')])),
                ('dependencia', models.ForeignKey(blank=True, to='visitas_stg.Dependencia', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='problematicasocial',
            options={'verbose_name': 'Problematica social', 'verbose_name_plural': 'Problematicas sociales'},
        ),
    ]
