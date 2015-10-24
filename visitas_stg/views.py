from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from visitas_stg.models import *
from visitas_stg.tools import *
from oauth2_provider.views import ProtectedResourceView

import os, sys
from pptx import Presentation
from django.core.servers.basehttp import FileWrapper
import mimetypes
from django.http import StreamingHttpResponse
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
from BuscarVisitas import BuscarVisitas, BuscaVisita

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
        sheet.write(0, 0, "id Unico", bold)
        sheet.write(0, 1, "Dependencia", bold)
        sheet.write(0, 2, "Fecha", bold)
        sheet.write(0, 3, "Region", bold)
        sheet.write(0, 4, "Entidad", bold)
        sheet.write(0, 5, "Municipio", bold)
        sheet.write(0, 6, "Distrito Electoral", bold)
        sheet.write(0, 7, "Partido Gobernante", bold)
        sheet.write(0, 8, "Funcionario", bold)
        sheet.write(0, 9, "Cargo de Funcionario", bold)
        sheet.write(0, 10, "Tipo de Actividad", bold)
        sheet.write(0, 11, "Descripcion", bold)
        sheet.write(0, 12, "Cargo de Funcionario", bold)

        i = 1
        for obra in json_ans['visitas']:
            sheet.write(i, 0, obra['identificador_unico'])
            sheet.write(i, 1, obra['dependencia']['nombreDependencia'])
            sheet.write(i, 2, obra['fecha_visita'])
            sheet.write(i, 3, obra['region']['numeroRegion'])
            sheet.write(i, 4, obra['entidad']['nombreEstado'])
            sheet.write(i, 5, obra['municipio']['nombreMunicipio'])
            sheet.write(i, 6, obra['distrito_electoral']['nombre_distrito_electoral'])
            sheet.write(i, 7, obra['partido_gobernante']['nombre_partido_gobernante'])
            sheet.write(i, 8, obra['cargo']['nombre_funcionario'])
            sheet.write(i, 9, obra['cargo']['nombre_cargo'])

            for actividad in obra['actividades']:
                sheet.write(i, 10, actividad['tipo_actividad']['nombre_actividad'])
                sheet.write(i, 11, actividad['descripcion'])
                sheet.write(i, 12, actividad['clasificacion']['nombre_clasificacion'])
                i += 1

        book.close()
    else:
        sheet.write(0, 0,
                   "Los filtros seleccionados no arrojaron informacion alguna sobre las obras, cambie los filtros para una nueva consulta.")
        book.close()

    response = StreamingHttpResponse(FileWrapper(output),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="listado_obras.xlsx"'
    response['Content-Length'] = output.tell()

    output.seek(0)

    return response


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

def usuarios(request):
    return render_to_response('admin/visitas_stg/usuarios.html', locals(),
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
        'Partidos': PartidoGobernante.objects.all(),
    })
    return HttpResponse(template.render(context))
    return render_to_response('admin/visitas_stg/consulta_filtros/consulta-filtros.html', locals(),
                              context_instance=RequestContext(request))

def fichaTecnica(request):
        #prs = Presentation('/home/obrasapf/djangoObras/obras/static/ppt/FichaTecnicaObras.pptx')
        prs = Presentation('visitas_stg/static/ppt/fichaTecnica_sisef.pptx')
        usuario = request.user.userprofile
        buscador = BuscaVisita(
            identificador_unico=request.GET.get('identificador_unico', None)
        )
        resultados = buscador.busca()

        json_map = {}
        json_map['visitas'] = []
        for visita in resultados['visitas']:
            json_map['visitas'].append(visita.to_serializable_dict())

        #generales
        prs.slides[0].shapes[3].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[3].text = json_map['visitas'][0]['identificador_unico']
        prs.slides[0].shapes[4].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[4].text = json_map['visitas'][0]['dependencia']['nombreDependencia']
        prs.slides[0].shapes[5].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[5].text = json_map['visitas'][0]['fecha_visita']
        prs.slides[0].shapes[6].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[6].text = json_map['visitas'][0]['region']['numeroRegion']
        prs.slides[0].shapes[7].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[7].text = json_map['visitas'][0]['entidad']['nombreEstado']
        prs.slides[0].shapes[8].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[8].text = json_map['visitas'][0]['municipio']['nombreMunicipio']
        prs.slides[0].shapes[9].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[9].text = json_map['visitas'][0]['distrito_electoral']['nombre_distrito_electoral']
        prs.slides[0].shapes[10].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[10].text = json_map['visitas'][0]['cargo']['nombre_funcionario']
        prs.slides[0].shapes[11].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[11].text = json_map['visitas'][0]['partido_gobernante']['nombre_partido_gobernante']
        prs.slides[0].shapes[12].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[12].text = json_map['visitas'][0]['cargo']['nombre_cargo']

        #detalles
        prs.slides[0].shapes[15].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[15].text = json_map['visitas'][0]['actividades'][0]['participantes_locales'][0]['nombre']
        prs.slides[0].shapes[16].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[16].text = json_map['visitas'][0]['actividades'][0]['participantes_locales'][0]['cargo']
        prs.slides[0].shapes[17].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[17].text = json_map['visitas'][0]['actividades'][0]['problematicas_sociales'][0]['problematica_social']
        prs.slides[0].shapes[18].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[18].text = json_map['visitas'][0]['actividades'][0]['capitalizaciones'][0]['medio']['nombre_medio']
        prs.slides[0].shapes[20].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[20].text = json_map['visitas'][0]['actividades'][0]['capitalizaciones'][0]['nombre_medio']
        prs.slides[0].shapes[19].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[19].text = json_map['visitas'][0]['actividades'][0]['capitalizaciones'][0]['tipo_capitalizacion']['nombre_tipo_capitalizacion']
        prs.slides[0].shapes[21].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[21].text = str(json_map['visitas'][0]['actividades'][0]['capitalizaciones'][0]['cantidad'])



        prs.save('visitas_stg/static/ppt/ppt-generados/FichaTecnicaObras_' + str(usuario.user.id) + '.pptx')

        the_file = 'visitas_stg/static/ppt/ppt-generados/FichaTecnicaObras_' + str(usuario.user.id) + '.pptx'

        filename = os.path.basename(the_file)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(the_file,"rb"), chunk_size),
                               content_type=mimetypes.guess_type(the_file)[0])
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
