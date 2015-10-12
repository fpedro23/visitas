from django.http import HttpResponse

# Create your views here.
from BuscarVisitas import BuscarVisitas


def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(int, the_string.split(','))


def buscar_visitas_web(request):
    buscador = BuscarVisitas(ids_dependencia=get_array_or_none(request.GET.get('dependencia')),
                             rango_fecha_inicio=request.GET.get('fechaInicio', None),
                             rango_fecha_fin=request.GET.get('fechaFin', None),
                             ids_region=get_array_or_none(request.GET.get('region')),
                             ids_entidad=get_array_or_none(request.GET.get('estado')),
                             ids_municipio=get_array_or_none(request.GET.get('municipio')),
                             ids_cargo_ejecuta=get_array_or_none(request.GET.get('cargoEjecuta')),
                             ids_distrito_electoral=get_array_or_none(request.GET.get('distritoElectoral')),
                             limite_min=request.GET.get('limiteMin', 0),
                             limite_max=request.GET.get('limiteMax', 100),
                             )

    resultados = buscador.buscar()
    print resultados

    return HttpResponse(resultados['visitas'])