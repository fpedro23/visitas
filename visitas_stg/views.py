from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from visitas_stg.models import *
from visitas_stg.tools import *
from oauth2_provider.views import ProtectedResourceView

from pptx import Presentation
from pptx.util import Inches
from pptx.util import Pt
from pptx.dml.color import RGBColor

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from xlsxwriter.workbook import Workbook
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse

# Create your views here.
from BuscarVisitas import BuscarVisitas

def get_user_for_token(token):
    if token:
        return AccessToken.objects.get(token=token).user
    else:
        return None

def register_by_access_token(request):

    #del request.session['access_token']

    if request.session.get('access_token'):
        token = {
        'access_token': request.session.get('access_token'),
        'token_type': 'Bearer'
    }
        return JsonResponse(token)
    else:
        #user = get_user_for_token('3DVteYz9OIH6gvQDyYX78GOpHKXgPy'
        user = request.user
        return get_access_token(user,request)




def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(int, the_string.split(','))

def listar_visitas(request):
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
    json_ans = {}
    json_ans['visitas'] = []
    for visita in resultados['visitas']:
        json_ans['visitas'].append(visita.to_serializable_dict())
    # Exportar a Excel

    output = StringIO.StringIO()
    book = Workbook(output)
    sheet = book.add_worksheet('Visitas')

    if resultados:
            # Add a bold format to use to highlight cells.
            bold = book.add_format({'bold': True})
            # encabezados
            sheet.write(0, 0, "Tipo de Obra", bold)
            sheet.write(0, 1, "id Unico", bold)
            sheet.write(0, 2, "Dependencia/Organismo", bold)
            sheet.write(0, 3, "Sub Dependencia", bold)
            sheet.write(0, 4, "Estado", bold)
            sheet.write(0, 5, "Denominacion", bold)
            sheet.write(0, 6, "Descripcion", bold)
            sheet.write(0, 7, "Municipio", bold)
            sheet.write(0, 8, "Fecha Inicio", bold)
            sheet.write(0, 9, "Fecha Termino", bold)
            sheet.write(0, 10, "Avance Fisico %", bold)
            sheet.write(0, 11, "F", bold)
            sheet.write(0, 12, "E", bold)
            sheet.write(0, 13, "M", bold)
            sheet.write(0, 14, "S", bold)
            sheet.write(0, 15, "P", bold)
            sheet.write(0, 16, "O", bold)
            sheet.write(0, 17, "Inversion Total", bold)
            sheet.write(0, 18, "Tipo Moneda MDP/MDD", bold)
            sheet.write(0, 19, "Registro de Cartera", bold)        #**************
            sheet.write(0, 20, "Poblacion Objetivo", bold)
            sheet.write(0, 21, "Numero de Beneficiarios", bold)
            sheet.write(0, 22, "Impacto", bold)
            sheet.write(0, 23, "CG", bold)
            sheet.write(0, 24, "PNG", bold)
            sheet.write(0, 25, "PM", bold)
            sheet.write(0, 26, "PNI", bold)
            sheet.write(0, 27, "CNCH", bold)
            sheet.write(0, 28, "OI", bold)
            sheet.write(0, 29, "Senalizacion", bold)
            sheet.write(0, 30, "Observaciones", bold)
            sheet.write(0, 31, "Inaugurado por:", bold)
            sheet.write(0, 32, "Inaugurado:", bold)
            sheet.write(0, 33, "Foto Antes", bold)
            sheet.write(0, 34, "Foto Durante", bold)
            sheet.write(0, 35, "Foto Despues", bold)
            sheet.write(0, 36, "Latitud", bold)
            sheet.write(0, 37, "Longitud", bold)


    return HttpResponse(resultados)

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
def movimientos(request):
    return render_to_response('admin/visitas_stg/movimientos.html', locals(),
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
