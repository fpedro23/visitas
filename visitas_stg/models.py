# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

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
        return {'id': self.id, 'numeroRegion': self.numeroRegion}


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
        return {'id': self.id, 'nombreEstado': self.nombreEstado, 'latitud': self.latitud, 'longitud': self.longitud,
                'region': self.region.to_serializable_dict()}


class DistritoElectoral(models.Model):
    nombre_distrito_electoral = models.CharField(max_length=200, verbose_name='Distrito Electoral')
    estado = models.ForeignKey(Estado, default=1, db_index=True)

    def __str__(self):
        return self.nombre_distrito_electoral

    def __unicode__(self):
        return self.nombre_distrito_electoral

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['estado'] = self.estado.to_serialzable_dict()
        return {'id': self.id, 'nombre_distrito_electoral': self.nombre_distrito_electoral,
                'estado': self.estado.to_serialzable_dict()}


class Municipio(models.Model):
    nombreMunicipio = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.ForeignKey(Estado, null=False, blank=False, db_index=True)
    distrito_electoral = models.ForeignKey(DistritoElectoral, default=1)

    def __str__(self):
        return self.nombreMunicipio

    def __unicode__(self):
        return self.nombreMunicipio

    def to_serializable_dict(self):
        ans = {}
        ans['nombreMunicipio'] = self.nombreMunicipio
        if self.latitud:
            ans['latitud'] = self.latitud
        else:
            ans['latidud'] = None
        if self.longitud:
            ans['longitud'] = self.longitud
        else:
            ans['longitud'] = None
        ans['estado'] = self.estado.to_serialzable_dict()
        return ans


class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.nombreDependencia

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nombreDependencia

    def to_serializable_dict(self):
        return {'id': self.id, 'nombreDependencia': self.nombreDependencia}

    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'


class Cargo(models.Model):  # Cargo de la persona que hace la actividad
    nombre_cargo = models.CharField(max_length=200)
    nombre_funcionario = models.CharField(max_length=200)
    dependencia = models.ForeignKey(Dependencia, default=1)

    def __str__(self):
        return self.nombre_cargo

    def __unicode__(self):
        return self.nombre_cargo

    def to_serializable_dict(self):
        return {'id': self.id, 'nombre_cargo': self.nombre_cargo, 'nombre_funcionario': self.nombre_funcionario,
                'dependencia': self.dependencia.to_serializable_dict()}

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'


class PartidoGobernante(models.Model):
    nombre_partido_gobernante = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_partido_gobernante

    def __unicode__(self):
        return self.nombre_partido_gobernante
    
    def to_serializable_dict(self):
        return {'id': self.id, 'nombre_partido_gobernante': self.nombre_partido_gobernante}


class Visita(models.Model):
    identificador_unico = models.SlugField(unique=True, null=True, verbose_name='Identificador Único')
    dependencia = models.ForeignKey(Dependencia, verbose_name='Dependencia', db_index=True)
    fecha_visita = models.DateField(verbose_name='Fecha de Visita')

    region = models.ForeignKey(Region, verbose_name='Región')
    entidad = ChainedForeignKey(Estado,
                                chained_field='region',
                                chained_model_field='region',
                                verbose_name='Entidad', db_index=True)
    municipio = ChainedForeignKey(Municipio,
                                  chained_field='entidad',
                                  chained_model_field='estado',
                                  verbose_name='Municipio')

    cargo = ChainedForeignKey(Cargo,
                              chained_field='dependencia',
                              chained_model_field='dependencia',
                              verbose_name='Cargo que ejecuta', db_index=True)

    distrito_electoral = models.ForeignKey(DistritoElectoral, verbose_name='Distrito electoral')
    partido_gobernante = models.ForeignKey(PartidoGobernante, null=True, blank=True, verbose_name='Partido Gobernante')

    def __str__(self):
        return self.cargo.nombre_funcionario + " - " + self.actividad_set.first().descripcion

    def __unicode__(self):
        return self.cargo.nombre_funcionario + " - " + self.actividad_set.first().descripcion

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def to_serializable_dict(self):
        ans = {}
        ans['id'] = self.id
        ans['identificador_unico'] = self.identificador_unico
        ans['dependencia'] = self.dependencia.to_serializable_dict()
        ans['region'] = self.region.to_serializable_dict()
        ans['entidad'] = self.entidad.to_serialzable_dict()
        ans['municipio'] = self.municipio.to_serializable_dict()
        ans['cargo'] = self.cargo.to_serializable_dict()
        ans['distrito_electoral'] = self.distrito_electoral.to_serializable_dict()
        ans['partido_gobernante'] = self.partido_gobernante.to_serializable_dict()
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
        return {'id': self.id, 'nombre_actividad': self.nombre_actividad}

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
        return {'id': self.id, 'nombre_clasificacion': self.nombre_clasificacion}

    class Meta:
        verbose_name = 'Clasificación'
        verbose_name_plural = 'Clasificaciones'


class Actividad(models.Model):
    tipo_actividad = models.ForeignKey(TipoActividad, verbose_name='Tipo de Actividad')
    descripcion = models.TextField(max_length=500, verbose_name='Descripción')
    clasificacion = models.ForeignKey(Clasificacion, verbose_name='Clasificación')
    visita = models.ForeignKey(Visita, default=1, db_index=True)

    def to_serializabe_dict(self):
        ans = {}
        ans['tipo_actividad'] = self.tipo_actividad.to_serializable_dict()
        ans['descripcion'] = self.descripcion
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
    problematica_social = models.TextField(max_length=200)
    actividad = models.ForeignKey(Actividad)

    def __str__(self):
        return self.problematica_social

    def __unicode__(self):
        return self.problematica_social

    def to_serializable_dict(self):
        ans = {}
        ans['id'] = self.id
        ans['problematica_social'] = self.problematica_social
        ans['actividad'] = self.actividad_id
        return ans

    class Meta:
        verbose_name = 'Problematica social'
        verbose_name_plural = 'Problematicas sociales'


# class CargoLocal(models.Model):  # Cargo de la persona Local
# nombre_cargo = models.CharField(max_length=200)
#
# def __str__(self):
# return self.nombre_cargo
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
        ans = {}
        ans['nombre'] = self.nombre
        ans['cargo'] = self.cargo
        ans['actividad'] = self.actividad_id
        return ans

    class Meta:
        verbose_name_plural = 'Participantes locales'
        verbose_name = 'Participante local'


class Medio(models.Model):
    nombre_medio = models.CharField(max_length=200, verbose_name='Tipo de Medio')

    def __str__(self):
        return self.nombre_medio

    def __unicode__(self):
        return self.nombre_medio

    def to_serializable_dict(self):
        return {'id': self.id, 'nombre_medio': self.nombre_medio}

    class Meta:
        verbose_name = 'Tipo de Medio'
        verbose_name_plural = 'Tipos de Medio'


class TipoCapitalizacion(models.Model):
    nombre_tipo_capitalizacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_tipo_capitalizacion

    def __unicode__(self):
        return self.nombre_tipo_capitalizacion

    def to_serializable_dict(self):
        return {'id': self.id, 'nombre_tipo_capitalizacion': self.nombre_tipo_capitalizacion}

    class Meta:
        verbose_name = 'Tipo de Capitalización'
        verbose_name_plural = 'Tipos de Capitalización'


class Capitalizacion(models.Model):
    medio = models.ForeignKey(Medio, verbose_name='Tipo de Medio')
    nombre_medio = models.CharField(max_length=200, null=True, blank=True, verbose_name='Nombre De Medio')
    tipo_capitalizacion = models.ForeignKey(TipoCapitalizacion)
    cantidad = models.PositiveIntegerField()
    evidencia_grafica = models.FileField(null=True, blank=True)
    actividad = models.ForeignKey(Actividad)


    def __str__(self):
        return self.tipo_capitalizacion.nombre_tipo_capitalizacion + ' - ' + self.medio.nombre_medio

    def __unicode__(self):
        return self.tipo_capitalizacion.nombre_tipo_capitalizacion + ' - ' + self.medio.nombre_medio

    def to_serializable_dict(self):
        ans = {}
        ans['medio'] = self.medio.to_serializable_dict()
        ans['nombre_medio'] = self.nombre_medio
        ans['tipo_capitalizacion'] = self.tipo_capitalizacion.to_serializable_dict()
        ans['cantidad'] = self.cantidad
        try:
            if self.evidencia_grafica is not None and self.evidencia_grafica.name is not None:
                ans['evidencia_grafica'] = self.evidencia_grafica.url
            else:
                ans['evidencia_grafica'] = None
        except ValueError:
            ans['evidencia_grafica'] = None
        ans['actividad'] = self.actividad_id
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
