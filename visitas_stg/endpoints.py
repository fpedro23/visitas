from django.db.models import Sum, IntegerField, Q
from django.db.models import F
from django.http import HttpResponse
from oauth2_provider.views import ProtectedResourceView
from BuscarVisitas import BuscarVisitas
from models import Estado, Municipio, TipoCapitalizacion, DistritoElectoral, Region, Cargo, Dependencia, \
    TipoActividad, Clasificacion, Medio, Visita, Capitalizacion, Actividad, ParticipanteLocal
import json
from oauth2_provider.models import AccessToken
from views import get_array_or_none


__author__ = 'mng687'


def get_usuario_for_token(token):
    if token:
        return AccessToken.objects.get(token=token).user.userprofile
    else:
        return None


class ReporteInicioEndpoint(ProtectedResourceView):
    def get(self, request):
        dependencia = get_usuario_for_token(request.GET.get('access_token')).dependencia
        if dependencia is None:
            visitas = Visita.objects.all()
            capitalizaciones = Capitalizacion.objects.all()
        else:
            visitas = Visita.objects.filter(dependencia=dependencia)
            capitalizaciones = Capitalizacion.objects.filter(actividad__visita__in=visitas)

        reporte = {}

        reporte['estados'] = []
        for estado in Estado.objects.all():
            reporte_estado = {'estado': estado.to_serialzable_dict(),
                              'total_visitas': visitas.filter(entidad=estado).count()}
            reporte['estados'].append(reporte_estado)

        reporte['medios'] = []
        for tipo_medio in Medio.objects.all():
            reporte_medio = {'medio': tipo_medio.to_serializable_dict(),
                             'total_apariciones': capitalizaciones.filter(medio=tipo_medio).aggregate(
                                 total=Sum('cantidad', output_field=IntegerField()))['total']}
            # 'total_apariciones': capitalizaciones.filter(medio=tipo_medio).count()}
            reporte['medios'].append(reporte_medio)

        return HttpResponse(json.dumps(reporte), 'application/json')


class ReporteEstadosEndpoint(ProtectedResourceView):
    def get(self, request):
        estado = Estado.objects.get(id=request.GET.get('estado_id'))

        map = {}
        map['estado'] = estado.to_serialzable_dict()
        map['estado']['distritos_electorales'] = DistritoElectoral.objects.filter(estado_id=estado.id).count()
        map['estado']['municipios'] = Municipio.objects.filter(estado_id=estado.id).count()

        map['dependencias'] = []
        dependencias = Dependencia.objects.all()
        for dependencia in dependencias:
            dependencia_map = dependencia.to_serializable_dict()
            dependencia_map['funcionarios_federales'] = Cargo.objects.filter(dependencia_id=dependencia.id).count()
            dependencia_map['visitas'] = Visita.objects.filter(
                Q(dependencia_id=dependencia.id) & Q(entidad_id=estado.id)).count()
            dependencia_map['actividades'] = Actividad.objects.filter(
                Q(visita__dependencia_id=dependencia.id) & Q(visita__entidad_id=dependencia.id)).count()
            dependencia_map['participantes_locales'] = ParticipanteLocal.objects.filter(
                Q(actividad__visita__dependencia_id=dependencia.id) & Q(actividad__visita__entidad_id=estado.id))
            dependencia_map['capitalizaciones'] = Capitalizacion.objects.filter(
                Q(actividad__visita__entidad_id=estado.id) & Q(
                    actividad__visita__dependencia_id=dependencia.id)).count()
            map['dependencias'].append(dependencia_map)

        map['medios'] = []
        medios = Medio.objects.all()
        for medio in medios:
            medio_map = medio.to_serializable_dict()

            medio_map['tipos_capitalizacion'] = []
            tipos_capitalizacion = TipoCapitalizacion.objects.all()
            for tipo_capitalizacion in tipos_capitalizacion:
                tipo_map = tipo_capitalizacion.to_serializable_dict()
                tipo_map['numero'] = Capitalizacion.objects.filter(
                    Q(tipo_capitalizacion_id=tipo_capitalizacion.id) & Q(medio_id=medio.id) & Q(
                        actividad__visita__entidad_id=estado.id)).count()
                medio_map['tipos_capitalizacion'].append(tipo_map)
            map['medios'].append(medio_map)

        return HttpResponse(json.dumps(map), 'application/json')


class ReporteDependenciasEndpoint(ProtectedResourceView):
    def get(self, request):
        dependencia = Dependencia.objects.get(id=request.GET.get('dependencia_id'))
        visitas = Visita.objects.filter(dependencia_id=dependencia.id)

        map = {}
        map['dependencia'] = dependencia.to_serializable_dict()
        map['dependencia']['estados_visitados'] = visitas.values('estado_id').distinct().count()
        map['dependencia']['municipios_visitados'] = visitas.values('entidad_id').distinct().count()
        map['dependencia']['distritos_electorales_visitados'] = visitas.values(
            'distrito_electoral_id').distinct().count()

        map['estados'] = []
        estados = Estado.objects.all()
        for estado in estados:
            estado_map = estado.to_serialzable_dict()
            estado_map['total_visitas_funcionarios_federales'] = Visita.objects.filter(
                Q(cargo__dependencia_id=dependencia.id) & Q(entidad_id=estado.id)).count()
            estado_map['total_visitas'] = Visita.objects.filter(
                Q(dependencia_id=dependencia.id) & Q(entidad_id=estado.id)).count()
            estado_map['total_actividades'] = Actividad.objects.filter(
                Q(visita__entidad_id=estado.id) & Q(visita__dependencia_id=dependencia.id)).count()
            estado_map['municipios'] = Visita.objects.filter(
                Q(dependencia_id=dependencia.id) & Q(entidad_id=dependencia.id)).values(
                'municipio_id').distinct().count()
            estado_map['participantes_locales'] = ParticipanteLocal.objects.filter(
                Q(actividad__visita__dependencia_id=dependencia.id) & Q(
                    actividad__visita__entidad_id=estado.id)).count()
            estado_map['capitalizaciones'] = Capitalizacion.objects.filter(
                Q(actividad__visita__dependencia_id=dependencia.id) & Q(actividad__visita__entidad_id=estado.id))
            map['estados'].append(estado_map)

            map['medios'] = []
            medios = Medio.objects.all()
            for medio in medios:
                medio_map = medio.to_serializable_dict()

                medio_map['tipos_capitalizacion'] = []
                tipos_capitalizacion = TipoCapitalizacion.objects.all()
                for tipo_capitalizacion in tipos_capitalizacion:
                    tipo_map = tipo_capitalizacion.to_serializable_dict()
                    tipo_map['numero'] = Capitalizacion.objects.filter(
                        Q(tipo_capitalizacion_id=tipo_capitalizacion.id) & Q(medio_id=medio.id) & Q(
                            actividad__visita__entidad_id=estado.id)).count()
                    medio_map['tipos_capitalizacion'].append(tipo_map)
                map['medios'].append(medio_map)

            return HttpResponse(json.dumps(map), 'application/json')

class RegionesEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda region: region.to_serializable_dict(), Region.objects.all())),
                            'application/json')


class EstadosForRegionesEndpoint(ProtectedResourceView):
    def get(self, request):
        region_ids = get_array_or_none(request.GET.get('regiones'))
        if region_ids is not None:
            estados = Estado.objects.filter(region_id__in=region_ids)
        else:
            estados = Estado.objects.all()

        return HttpResponse(json.dumps(map(lambda estado: estado.to_serialzable_dict(), estados)), 'application/json')


class MunicipiosForEstadosEndpoint(ProtectedResourceView):
    def get(self, request):
        estado_ids = get_array_or_none(request.GET.get('estados'))
        if estado_ids is not None:
            municipios = Municipio.objects.filter(estado_id__in=estado_ids)
        else:
            municipios = Municipio.objects.all()

        the_list = []
        for municipio in municipios.values('id', 'nombreMunicipio'):
            the_list.append(municipio)

        return HttpResponse(json.dumps(the_list), 'application/json')


class DistritoElectoralForEstadosEndpoint(ProtectedResourceView):
    def get(self, request):
        estado_ids = get_array_or_none(request.GET.get('estados'))

        if estado_ids is not None:
            distritos = DistritoElectoral.objects.filter(estado_id__in=estado_ids)
        else:
            distritos = DistritoElectoral.objects.all()

        return HttpResponse(json.dumps(map(lambda distrito: distrito.to_serializable_dict(), distritos)),
                            'application/json')


class CargosForDependenciasEndpoint(ProtectedResourceView):
    def get(self, request):
        dependencia_ids = get_array_or_none(request.GET.get('dependencias'))

        if dependencia_ids is not None and len(dependencia_ids) > 0:
            cargos = Cargo.objects.filter(dependencia_id__in=dependencia_ids)
        else:
            cargos = Cargo.objects.all()

        return HttpResponse(json.dumps(map(lambda cargo: cargo.to_serializable_dict(), cargos)), 'application/json')


class CargosForCargosEndpoint(ProtectedResourceView):
    def get(self, request):
        cargos_string = request.GET.get('cargos', None)

        if cargos_string is None:
            cargos_nombres = None
        else:
            cargos_nombres = cargos_string.split(',')

        if cargos_nombres is not None and len(cargos_nombres) > 0:
            cargos = Cargo.objects.all()
        else:
            cargos = Cargo.objects.filter(nombre_cargo__in=cargos_nombres)

        return HttpResponse(json.dumps(map(lambda cargo: cargo.to_serializable_dict(), cargos)), 'application/json')


class BuscarVisitasEndpoint(ProtectedResourceView):
    def get(self, request):
        buscador = BuscarVisitas(ids_dependencia=get_array_or_none(request.GET.get('dependencia')),
                                 rango_fecha_inicio=request.GET.get('fechaInicio', None),
                                 rango_fecha_fin=request.GET.get('fechaFin', None),
                                 descripcion=request.GET.get('descripcion', None),
                                 problematica=request.GET.get('problematica', None),
                                 nombre_medio=request.GET.get('nombreMedio', None),
                                 ids_region=get_array_or_none(request.GET.get('region')),
                                 ids_entidad=get_array_or_none(request.GET.get('estado')),
                                 ids_municipio=get_array_or_none(request.GET.get('municipio')),
                                 ids_cargo_ejecuta=get_array_or_none(request.GET.get('cargoEjecuta')),
                                 ids_distrito_electoral=get_array_or_none(request.GET.get('distritoElectoral')),
                                 ids_partido=get_array_or_none(request.GET.get('partido')),
                                 identificador_unico=request.GET.get('identificador_unico', None),
                                 ids_tipo_actividad=get_array_or_none(request.GET.get('tipoActividad')),
                                 ids_tipo_medio=get_array_or_none(request.GET.get('tipoMedio')),
                                 ids_tipo_capitalizacion=get_array_or_none(request.GET.get('tipoCapitalizacion')),
                                 ids_clasificacion=get_array_or_none(request.GET.get('tipoClasificacion')),
                                 limite_min=request.GET.get('limiteMin', 0),
                                 limite_max=request.GET.get('limiteMax', 100),
                                 )
        ans = buscador.buscar()

        json_ans = {}
        json_ans['visitas'] = []
        for visita in ans['visitas']:
            json_ans['visitas'].append(visita.to_serializable_dict())

        json_ans['reporte_general'] = {'visitas_totales': ans['reporte_general']['visitas_totales']}

        json_ans['reporte_estado'] = []
        for estado in ans['reporte_estado']:
            json_map = {'estado': estado['entidad__nombreEstado'],
                        'numero_visitas': estado['numero_visitas']}
            json_ans['reporte_estado'].append(json_map)

        json_ans['reporte_dependencia'] = []
        for dependencia in ans['reporte_dependencia']:
            json_map = {'dependencia': dependencia['dependencia__nombreDependencia'],
                        'numero_visitas': dependencia['numero_visitas']}
            json_ans['reporte_dependencia'].append(json_map)

        return HttpResponse(json.dumps(json_ans), 'application/json')


class DependenciasEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(
            json.dumps(map(lambda dependencia: dependencia.to_serializable_dict(), Dependencia.objects.all())),
            'application/json')


class TipoActividadEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda tipo: tipo.to_serializable_dict(), TipoActividad.objects.all())),
                            "application/json")


class ClasificacionEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(
            json.dumps(map(lambda clasificacion: clasificacion.to_serializable_dict(), Clasificacion.objects.all())),
            'application/json')


class MediosEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda medio: medio.to_serializable_dict(), Medio.objects.all())),
                            'application/json')


class TipoCapitalizacionEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(
            json.dumps(map(lambda tipoCapitalizacion: tipoCapitalizacion.to_serializable_dict(),
                           TipoCapitalizacion.objects.all())), 'application/json')