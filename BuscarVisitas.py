from django.db.models import Q, Count

__author__ = 'Pedro'

from visitas_stg.models import *


class BuscarVisitas:
    def __init__(
            self,
            ids_dependencia,
            rango_fecha_inicio,
            rango_fecha_fin,
            ids_region,
            ids_entidad,
            ids_municipio,
            ids_cargo_ejecuta,
            ids_distrito_electoral,
            limite_min,
            limite_max,
    ):

        self.dependencias = ids_dependencia
        self.fecha_inicio = rango_fecha_inicio
        self.fecha_fin = rango_fecha_fin

        self.regiones = ids_region
        self.entidades = ids_entidad
        self.municipios = ids_municipio
        self.cargos_ejecuta = ids_cargo_ejecuta
        self.distritos_electorales = ids_distrito_electoral
        self.limite_min = limite_min
        self.limite_max = limite_max

    def buscar(self):
        query = Q()

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

        if query is not None:
            visitas = Visita.objects.filter(query)

        # Reporte General
        visitas_totales = visitas.count()

        # Reporte Dependencia
        reporte_dependencia = visitas.values('dependencia__nombreDependencia').annotate(
            numero_visitas=Count('dependencia'))

        reporte_estado = visitas.values('entidad__nombreEstado').annotate(numero_visitas=Count('entidad'))

        reporte_general = {
            'visitas_totales': visitas_totales,
        }

        reportes = {
            'visitas': visitas[self.limite_min:self.limite_max],
            'reporte_general': reporte_general,
            'reporte_dependencia': reporte_dependencia,
            'reporte_estado': reporte_estado,
        }

        return reportes