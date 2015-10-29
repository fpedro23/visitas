from django.db.models import Q, Count, Sum

__author__ = 'Pedro'

from visitas_stg.models import *


class BuscarVisitas:
    def __init__(
            self,
            identificador_unico,
            descripcion,
            problematica,
            nombre_medio,
            ids_dependencia,
            rango_fecha_inicio,
            rango_fecha_fin,
            ids_region,
            ids_entidad,
            ids_municipio,
            ids_cargo_ejecuta,
            ids_distrito_electoral,
            ids_tipo_actividad,
            ids_tipo_medio,
            ids_tipo_capitalizacion,
            ids_clasificacion,
            ids_partido,
            limite_min,
            limite_max,
    ):
        self.identificador_unico = identificador_unico
        self.descripcion = descripcion
        self.dependencias = ids_dependencia
        self.fecha_inicio = rango_fecha_inicio
        self.fecha_fin = rango_fecha_fin
        self.ids_tipo_actividad = ids_tipo_actividad
        self.ids_tipo_medio = ids_tipo_medio
        self.ids_tipo_capitalizacion = ids_tipo_capitalizacion
        self.ids_clasificacion = ids_clasificacion
        self.problematica = problematica
        self.nombre_medio = nombre_medio
        self.regiones = ids_region
        self.entidades = ids_entidad
        self.municipios = ids_municipio
        self.cargos_ejecuta = ids_cargo_ejecuta
        self.distritos_electorales = ids_distrito_electoral
        self.ids_partido = ids_partido

        self.limite_min = limite_min
        self.limite_max = limite_max

    def buscar(self):
        query = Q()

        if self.identificador_unico is not None:
            query = query & Q(identificador_unico=self.identificador_unico)

        if self.descripcion is not None:
            query = query & Q(actividad__descripcion__icontains=self.descripcion)

        if self.nombre_medio is not None:
            query = query & Q(actividad__capitalizacion__nombre_medio__icontains=self.nombre_medio)

        if self.problematica is not None:
            query = query & Q(actividad__problematicasocial__problematica_social__icontains=self.problematica)

        if self.ids_tipo_actividad is not None:
            query = query & Q(actividad__tipo_actividad__id__in=self.ids_tipo_actividad)

        if self.ids_clasificacion is not None:
            query = query & Q(actividad__clasificacion__id__in=self.ids_clasificacion)

        if self.ids_tipo_medio is not None:
            query = query & Q(actividad__capitalizacion__medio__id__in=self.ids_tipo_medio)

        if self.ids_tipo_capitalizacion is not None:
            query = query & Q(actividad__capitalizacion__tipo_capitalizacion__id__in=self.ids_tipo_capitalizacion)

        if self.dependencias is not None:
            query = query & Q(dependencia_id__in=self.dependencias)

        if self.fecha_inicio is not None and self.fecha_fin is not None:
            query = query & Q(fecha_visita__range=(self.fecha_inicio, self.fecha_fin))

        if self.fecha_inicio is not None and self.fecha_fin is None:
            query = query & Q(fecha_visita__gte=self.fecha_inicio)

        if self.fecha_fin is not None and self.fecha_inicio is None:
            query = query & Q(fecha_visita__lte=self.fecha_fin)

        if self.regiones is not None:
            query = query & Q(region_id__in=self.regiones)

        if self.entidades is not None:
            query = query & Q(entidad_id__in=self.entidades)

        if self.municipios is not None:
            query = query & Q(municipio_id__in=self.municipios)

        if self.cargos_ejecuta is not None:
            query = query & Q(cargo_id__in=self.cargos_ejecuta)

        if self.distritos_electorales is not None:
            query = query & Q(distrito_electoral_id__in=self.distritos_electorales)

        if self.ids_partido is not None:
            print self.ids_partido
            query = query & Q(partido_gobernante_id__in=self.ids_partido)

        if query is not None:
            visitas = Visita.objects.filter(query).distinct().order_by('identificador_unico')

        # Reporte General
        visitas_totales = visitas.count()

        # Reporte Dependencia
        reporte_dependencia = visitas.values('dependencia__nombreDependencia').annotate(
            numero_visitas=Count('dependencia'), numero_apariciones=Sum('actividad__capitalizacion__cantidad'))

        reporte_estado = visitas.values('entidad__nombreEstado').annotate(numero_visitas=Count('entidad')).annotate(
            numero_apariciones=Sum('actividad__capitalizacion__cantidad'))

        reporte_municipio = visitas.values('municipio_id', 'municipio__nombreMunicipio', 'municipio__latitud',
                                           'municipio__longitud', 'entidad__nombreEstado').distinct().annotate(
            numero_visitas=Count('id', distinct=True),
            numero_apariciones=Sum('actividad__capitalizacion__cantidad'))
        for municipio in reporte_municipio:
            municipio['visitas'] = visitas_municipio = visitas.filter(municipio_id=municipio['municipio_id']).values(
                'identificador_unico')

        reporte_general = {
            'visitas_totales': visitas_totales,
        }

        reportes = {
            'visitas': visitas[self.limite_min:self.limite_max],
            'reporte_general': reporte_general,
            'reporte_dependencia': reporte_dependencia,
            'reporte_estado': reporte_estado,
            'reporte_municipio': reporte_municipio
        }

        return reportes


class BuscaVisita:
    def __init__(
            self,
            identificador_unico,
    ):
        self.identificador_unico = identificador_unico

    def busca(self):
        query = Q()

        if self.identificador_unico is not None:
            query = query & Q(identificador_unico=self.identificador_unico)

        if query is not None:
            visitas = Visita.objects.filter(query).distinct()

        reportes = {
            'visitas': visitas,
        }

        return reportes