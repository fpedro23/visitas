import json
from django.db.models import Count, Q, Sum
from visitas_stg.models import Dependencia, Visita, ParticipanteLocal, Capitalizacion, Clasificacion, Actividad

__author__ = 'mng687'


def generar_reporte_dependencias(dependencia_ids):
    ans = []
    if dependencia_ids is None or len(dependencia_ids) == 0:
        dependencias = Dependencia.objects.all()
    else:
        dependencias = Dependencia.objects.filter(id__in=dependencia_ids)
    dependencias = dependencias.values('id', 'nombreDependencia')

    for dependencia in dependencias:
        dependencia_map = dependencia

        visitas = Visita.objects.filter(dependencia_id=dependencia['id'])
        capitalizaciones = Capitalizacion.objects.filter(actividad__visita__dependencia_id=dependencia['id'])

        dependencia_map['estados_visitados'] = visitas.values('entidad_id').distinct().count()
        dependencia_map['municipios_visitados'] = visitas.values('municipio_id').distinct().count()
        dependencia_map['distritos_electorales_visitados'] = visitas.values('distrito_electoral_id').distinct().count()

        dependencia_map['estados'] = []
        estados = visitas.values('entidad_id', 'entidad__nombreEstado').distinct().annotate(
            total_visitas=Count('id', distinct=True),
            total_actividades=Count('actividad', distinct=True),
            municipios=Count('municipio_id', distinct=True),
            capitalizaciones=Count('actividad__capitalizacion', distinct=True)
        )

        for estado in estados:
            estado_map = estado
            estado['participantes_locales'] = ParticipanteLocal.objects.filter(
                Q(actividad__visita__entidad_id=estado['entidad_id'])
                & Q(actividad__visita__dependencia_id=dependencia['id'])).count()
            estado['total_visitas_funcionarios_federales'] = Visita.objects.filter(
                Q(cargo__dependencia_id=dependencia['id']) & Q(entidad_id=estado['entidad_id'])).count()
            dependencia_map['estado'].append[estado_map]

        dependencia_map['medios'] = capitalizaciones.values('medio_id', 'medio__nombre_medio').distinct()
        for medio in dependencia['medios']:
            medio['tipos_capitalizacion'] = capitalizaciones.filter(medio_id=medio['medio_id']).values(
                'tipo_capitalizacion_id',
                'tipo_capitalizacion__nombre_tipo_capitalizacion').distinct().annotate(
                numero_capitalizaciones=Count('id', distinct=True), numero_apariciones=Sum('cantidad'))

        dependencia_map['clasificaciones'] = Clasificacion.objects.values('id', 'nombre_clasificacion')
        for clasificacion in dependencia['clasificaciones']:
            clasificacion['numero'] = Actividad.objects.filter(
                Q(visita__dependencia_id=dependencia['id']) & Q(clasificacion_id=clasificacion['id'])).count()
        ans.append(dependencia_map)
    return json.dumps(ans)


generar_reporte_dependencias([1])