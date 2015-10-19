from django.http import HttpResponse
from oauth2_provider.views import ProtectedResourceView
from visitas_stg.models import Estado, Municipio, TipoCapitalizacion
import json
from visitas_stg.views import get_array_or_none


__author__ = 'mng687'

class EstadosEndpoint(ProtectedResourceView):
    def get(self, request):
        return HttpResponse(json.dumps(map(lambda estado: estado.to_serializable_dict(), Estado.objects.all())),
                            'application/json')


class MunicipiosForEstadosEndpoint(ProtectedResourceView):

    def get(self, request):
        estado_ids = get_array_or_none(request.GET.get('estados'))
        all_estados = False

        if estado_ids is None:
            all_estados = True
        else:
            for estado_id in estado_ids:
                if estado_id == 33 or estado_id == 34:
                    all_estados = True
                    break

        if all_estados:
            municipios = Municipio.objects.all()
        else:
            municipios = Municipio.objects.filter(estado_id__in=estado_ids)

        the_list = []
        for municipio in municipios.values('id', 'nombreMunicipio'):
            the_list.append(municipio)

        return HttpResponse(json.dumps(the_list), 'application/json')

class TipoCapitalizacionEndpoint(ProtectedResourceView):

    def get(self, request):
        return HttpResponse(json.dumps(map(lambda tipoCapitalizacion: tipoCapitalizacion.to_serializable_dict(), TipoCapitalizacion.objects.all())))
