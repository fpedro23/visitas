from django.http import HttpResponse

# Create your views here.
from BuscarVisitas import BuscarVisitas


def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(int, the_string.split(','))


def listar_obras(request):
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

    resultados = buscador.buscar()

    # Exportar a Excel

    return HttpResponse(resultados)

def buscar_visitas_web(request):
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

    resultados = buscador.buscar()
    print resultados

    return HttpResponse(resultados['visitas'])