# coding=utf-8
from django.db import models

# Create your models here.


class Region(models.Model):
    numeroRegion = models.CharField(max_length=2)

    def __str__(self):  # __unicode__ on Python 2
        return self.numeroRegion

    def __unicode__(self):  # __unicode__ on Python 2
        return self.numeroRegion


class Estado(models.Model):
    nombreEstado = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    region = models.ForeignKey(Region, null=False, blank=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nombreEstado


class Municipio(models.Model):
    nombreMunicipio = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.ForeignKey(Estado, null=False, blank=False)

    def __str__(self):
        return self.nombreMunicipio

    def __unicode__(self):
        return self.nombreMunicipio


class Cargo(models.Model):  # Cargo de la persona que hace la actividad
    nombre_cargo = models.CharField(max_length=200)
    nombre_funcionario = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_cargo + "-" + self.nombre_funcionario

    def __unicode__(self):
        return self.nombre_cargo + "-" + self.nombre_funcionario


class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreDependencia


class Visita(models.Model):
    dependencia = models.ForeignKey(Dependencia, default=1)
    fecha_visita = models.DateField('Fecha')
    region = models.ForeignKey(Region)
    entidad = models.ForeignKey(Estado)
    municipio = models.ForeignKey(Municipio)
    cargo = models.ForeignKey(Cargo)

    def __str__(self):
        return self.cargo.nombre_funcionario + " - " + self.actividad_set.first().descripcion

    def __unicode__(self):
        return self.cargo.nombre_funcionario + " - " + self.actividad_set.first().descripcion


class TipoActividad(models.Model):
    nombre_actividad = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_actividad

    def __unicode__(self):
        return self.nombre_actividad


class Clasificacion(models.Model):
    nombre_clasificacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_clasificacion

    def __unicode__(self):
        return self.nombre_clasificacion


class Actividad(models.Model):
    tipo_actividad = models.ForeignKey(TipoActividad)
    descripcion = models.CharField(max_length=200)
    clasificacion = models.ForeignKey(Clasificacion)
    problematica = models.CharField(max_length=200)
    visita = models.ForeignKey(Visita, default=1)

    class Meta:
        verbose_name_plural = "Actividades"
        verbose_name = "Actividad"


class CargoLocal(models.Model):  # Cargo de la persona Local
    nombre_cargo = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_cargo

    def __unicode__(self):
        return self.nombre_cargo


class ParticipanteLocal(models.Model):
    nombre = models.CharField(max_length=200)
    cargo = models.ForeignKey(CargoLocal)
    actividad = models.ForeignKey(Actividad)

    class Meta:
        verbose_name_plural = 'Participantes locales'
        verbose_name = 'Participante local'


class Medio(models.Model):
    nombre_medio = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_medio

    def __unicode__(self):
        return self.nombre_medio


class TipoCapitalizacion(models.Model):
    nombre_tipo_capitalizacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_tipo_capitalizacion

    def __unicode__(self):
        return self.nombre_tipo_capitalizacion


class Capitalizacion(models.Model):
    medio = models.ForeignKey(Medio)
    tipo_capitalizacion = models.ForeignKey(TipoCapitalizacion)
    cantidad = models.PositiveIntegerField()
    evidencia_grafica = models.FileField(null=True, blank=True)
    actividad = models.ForeignKey(Actividad)

    class Meta:
        verbose_name_plural = 'Capitalización'
        verbose_name = 'Capitalización'


