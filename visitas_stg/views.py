from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from visitas_stg.models import *

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

    return HttpResponse(resultados['visitas_stg'])

def catalogos(request):
    return render_to_response('admin/visitas_stg/catalogos.html', locals(),
                              context_instance=RequestContext(request))

def catalogo_funcionarios(request):
    return render_to_response('admin/visitas_stg/catalogo_funcionarios.html', locals(),
                              context_instance=RequestContext(request))

def catalogo_medios(request):
    return render_to_response('admin/visitas_stg/catalogo_medios.html', locals(),
                              context_instance=RequestContext(request))

def catalogo_tipoActividad(request):
    return render_to_response('admin/visitas_stg/catalogo_tipoActividad.html', locals(),
                              context_instance=RequestContext(request))

def catalogo_capitalizacion(request):
    return render_to_response('admin/visitas_stg/catalogo_capitalizacion.html', locals(),
                              context_instance=RequestContext(request))

def consultas(request):
    return render_to_response('admin/visitas_stg/consultas.html', locals(),
                              context_instance=RequestContext(request))
def consulta_filtros(request):

    template = loader.get_template('admin/visitas_stg/consulta_filtros/consulta-filtros.html')
    context = RequestContext(request, {
        'Regiones': Region.objects.all(),
        'Estados': Estado.objects.all(),
        'Distritos': DistritoElectoral.objects.all(),
        'Municipios': Municipio.objects.all(),
        'Funcionarios': Cargo.objects.all(),
        'Dependencias': Dependencia.objects.all(),
        'TipoActividad': TipoActividad.objects.all(),
        'TipoCapitalizacion': TipoCapitalizacion.objects.all(),
        'Medios': Medio.objects.all(),
        'Clasificaciones': Clasificacion.objects.all(),
    })
    return HttpResponse(template.render(context))
    return render_to_response('admin/visitas_stg/consulta_filtros/consulta-filtros.html', locals(),
                              context_instance=RequestContext(request))
