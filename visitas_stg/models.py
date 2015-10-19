# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import model_to_dict


class Region(models.Model):
    numeroRegion = models.CharField(max_length=2)

    def __str__(self):  # __unicode__ on Python 2
        return self.numeroRegion

    def __unicode__(self):  # __unicode__ on Python 2
        return self.numeroRegion

    class Meta:
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'

    def to_serializable_dict(self):
        return model_to_dict(self)


class Estado(models.Model):
    nombreEstado = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    region = models.ForeignKey(Region, null=False, blank=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nombreEstado

    def to_serialzable_dict(self):
        ans = model_to_dict(self)
        ans['region'] = self.region.to_serializable_dict()
        return ans


class DistritoElectoral(models.Model):
    nombre_distrito_electoral = models.CharField(max_length=200, verbose_name='Distrito Electoral')
    estado = models.ForeignKey(Estado, default=1)

    def __str__(self):
        return self.nombre_distrito_electoral

    def __unicode__(self):
        return self.nombre_distrito_electoral

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['estado'] = self.estado.to_serialzable_dict()
        return ans


class Municipio(models.Model):
    nombreMunicipio = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.ForeignKey(Estado, null=False, blank=False)

    def __str__(self):
        return self.nombreMunicipio

    def __unicode__(self):
        return self.nombreMunicipio

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['estado'] = self.estado.to_serialzable_dict()
        return ans


class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreDependencia

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nombreDependencia

    def to_serializable_dict(self):
        return model_to_dict(self)

    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'


class Cargo(models.Model):  # Cargo de la persona que hace la actividad
    nombre_cargo = models.CharField(max_length=200)
    nombre_funcionario = models.CharField(max_length=200)
    dependencia = models.ForeignKey(Dependencia)

    def __str__(self):
        return self.nombre_cargo + " - " + self.nombre_funcionario

    def __unicode__(self):
        return self.nombre_cargo + " - " + self.nombre_funcionario

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['dependencia'] = self.dependencia.to_serializable_dict()

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'




class Visita(models.Model):
    dependencia = models.ForeignKey(Dependencia, default=1, verbose_name='Dependencia')
    fecha_visita = models.DateField(verbose_name='Fecha de Visita')
    region = models.ForeignKey(Region, verbose_name='Región')
    entidad = models.ForeignKey(Estado, verbose_name='Entidad')
    municipio = models.ForeignKey(Municipio, verbose_name='Municipio')
    cargo = models.ForeignKey(Cargo, verbose_name='Cargo que ejecuta')
    distrito_electoral = models.ForeignKey(DistritoElectoral, default=0, verbose_name='Distrito electoral')
    partido_gobernante = models.CharField(max_length=200, null=True, blank=True, verbose_name='Partido Gobernante')

    def __str__(self):
        return self.cargo.nombre_funcionario + " - " + self.actividad_set.first().descripcion

    def __unicode__(self):
        return self.cargo.nombre_funcionario + " - " + self.actividad_set.first().descripcion

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['dependencia'] = self.dependencia.to_serializable_dict()
        ans['fecha_visita'] = self.fecha_visita.__str__()

        ans['actividades'] = []
        actividades = Actividad.objects.filter(visita_id=self.id).all()
        for actividad in actividades:
            ans['actividades'].append(actividad.to_serializabe_dict())

        return ans


class TipoActividad(models.Model):
    nombre_actividad = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_actividad

    def __unicode__(self):
        return self.nombre_actividad

    def to_serializable_dict(self):
        return model_to_dict(self)

    class Meta:
        verbose_name = 'Tipo de Actividad'
        verbose_name_plural = 'Tipos de Actividad'


class Clasificacion(models.Model):
    nombre_clasificacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_clasificacion

    def __unicode__(self):
        return self.nombre_clasificacion

    def to_serializable_dict(self):
        return model_to_dict(self)

    class Meta:
        verbose_name = 'Clasificación'
        verbose_name_plural = 'Clasificaciones'


class Actividad(models.Model):
    tipo_actividad = models.ForeignKey(TipoActividad, verbose_name='Tipo de Actividad')
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    clasificacion = models.ForeignKey(Clasificacion, verbose_name='Clasificación')
    visita = models.ForeignKey(Visita, default=1)

    def to_serializabe_dict(self):
        ans = model_to_dict(self)
        ans['tipo_actividad'] = self.tipo_actividad.to_serializable_dict()
        ans['clasificacion'] = self.clasificacion.to_serializable_dict()
        ans['visita'] = self.visita_id

        ans['capitalizaciones'] = []
        capitalizaciones = Capitalizacion.objects.filter(actividad_id=self.id).all()
        for capitalizacion in capitalizaciones:
            ans['capitalizaciones'].append(capitalizacion.to_serializable_dict())

        ans['problematicas_sociales'] = []
        problematicas = ProblematicaSocial.objects.filter(actividad_id=self.id).all()
        for capitalizacion in problematicas:
            ans['problematicas_sociales'].append(capitalizacion.to_serializable_dict())

        ans['participantes_locales'] = []
        participantes = ParticipanteLocal.objects.filter(actividad_id=self.id).all()
        for participante in participantes:
            ans['participantes_locales'].append(participante.to_serializable_dict())

        return ans

    class Meta:
        verbose_name_plural = "Actividades"
        verbose_name = "Actividad"


class ProblematicaSocial(models.Model):
    problematica_social = models.CharField(max_length=200)
    actividad = models.ForeignKey(Actividad)

    def __str__(self):
        return self.problematica_social

    def __unicode__(self):
        return self.problematica_social

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['actividad'] = self.actividad_id
        return ans

    class Meta:
        verbose_name = 'Problematica social'
        verbose_name_plural = 'Problematicas sociales'


# class CargoLocal(models.Model):  # Cargo de la persona Local
#     nombre_cargo = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.nombre_cargo
#
#     def __unicode__(self):
#         return self.nombre_cargo
#
#     class Meta:
#         verbose_name = 'Cargo local'
#         verbose_name_plural = 'Cargos locales'


class ParticipanteLocal(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre de participante local')
    cargo = models.CharField(max_length=200, verbose_name='Cargo del participante local')
    actividad = models.ForeignKey(Actividad)

    def __str__(self):
        return self.nombre + ' - ' + self.cargo

    def __unicode__(self):
        return self.nombre + ' - ' + self.cargo

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['actividad'] = self.actividad_id
        return ans

    class Meta:
        verbose_name_plural = 'Participantes locales'
        verbose_name = 'Participante local'


class Medio(models.Model):
    nombre_medio = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_medio

    def __unicode__(self):
        return self.nombre_medio

    def to_serializable_dict(self):
        return model_to_dict(self)

    class Meta:
        verbose_name = 'Medio'
        verbose_name_plural = 'Medios'


class TipoCapitalizacion(models.Model):
    nombre_tipo_capitalizacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_tipo_capitalizacion

    def __unicode__(self):
        return self.nombre_tipo_capitalizacion

    def to_serializable_dict(self):
        return model_to_dict(self)

    class Meta:
        verbose_name = 'Tipo de Capitalización'
        verbose_name_plural = 'Tipos de Capitalización'


class Capitalizacion(models.Model):
    medio = models.ForeignKey(Medio)
    tipo_capitalizacion = models.ForeignKey(TipoCapitalizacion)
    cantidad = models.PositiveIntegerField()
    evidencia_grafica = models.FileField(null=True, blank=True)
    actividad = models.ForeignKey(Actividad)

    def __str__(self):
        return self.tipo_capitalizacion.nombre_tipo_capitalizacion + ' - ' + self.medio.nombre_medio

    def __unicode__(self):
        return self.tipo_capitalizacion.nombre_tipo_capitalizacion + ' - ' + self.medio.nombre_medio

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['medio'] = self.medio.to_serializable_dict()
        ans['tipo_capitalizacion'] = self.tipo_capitalizacion.to_serializable_dict()
        if self.evidencia_grafica is not None and self.evidencia_grafica.name is not None:
            ans['evidencia_grafica'] = self.evidencia_grafica.url
        else:
            ans['evidencia_grafica'] = None
        return ans

    class Meta:
        verbose_name_plural = 'Capitalizaciones'
        verbose_name = 'Capitalización'


class UserProfile(models.Model):
    ADMIN = 'AD'
    USER = 'US'

    ROLES_CHOICES = (
        (ADMIN, 'Administrador general'),
        (USER, 'Usuario de Dependencia'),
    )
    rol = models.CharField(max_length=2, choices=ROLES_CHOICES, default=USER)
    user = models.OneToOneField(User)
    dependencia = models.ForeignKey(Dependencia, blank=True, null=True, )
