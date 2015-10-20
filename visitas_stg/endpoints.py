from django.http import HttpResponse
from oauth2_provider.views import ProtectedResourceView
from BuscarVisitas import BuscarVisitas
from models import Estado, Municipio, TipoCapitalizacion, DistritoElectoral, Region, Cargo, Dependencia, \
    TipoActividad, Clasificacion, Medio
import json
from views import get_array_or_none


__author__ = 'mng687'


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

        json_ans['repote_estado'] = []
        for estado in ans['reporte_estado']:
            json_map = {'estado': estado['estado__nombreEstado'],
                        'numero_visitas': estado['numero_visitas']}
            json_ans.append(json_map)

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