from django.conf.urls import patterns, include, url
from django.contrib import admin

from visitas_stg import  views, endpoints


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'visitas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^busqueda-filtros/', views.buscar_visitas_web, name='consulta_filtros'),
    url(r'^visitas_stg/movimientos$', 'visitas_stg.views.movimientos', name='movimientos'),
    url(r'^visitas/catalogos$', 'visitas_stg.views.catalogos', name='catalogos'),
    url(r'^visitas/catalogo-funcionarios$', 'visitas_stg.views.catalogo_funcionarios', name='catalogo_funcionarios'),
    url(r'^visitas/catalogo-medios$', 'visitas_stg.views.catalogo_medios', name='catalogo_medios'),
    url(r'^visitas/catalogo-tipoActividad$', 'visitas_stg.views.catalogo_tipoActividad', name='catalogo_tipoActividad'),
    url(r'^visitas/catalogo-capitalizacion$', 'visitas_stg.views.catalogo_capitalizacion', name='catalogo_capitalizacion'),
    url(r'^visitas/consultas$', 'visitas_stg.views.consultas', name='consultas'),
    url(r'^visitas/consulta_filtros$', 'visitas_stg.views.consulta_filtros', name='consulta_filtros'),
    url(r'^visitas/busqueda-filtros', views.buscar_visitas_web, name='consulta_filtros'),
    url(r'^visitas/register-by-token$',views.register_by_access_token),
    url(r'^visitas/listar-visitas', views.listar_visitas, name='listar_visitas'),





    url(r'^api/ReportePP', endpoints.PptxReporteEndpoint.as_view()),
    url(r'^api/PptxVista', endpoints.PptxEndpoint.as_view()),
    url(r'^api/buscador', endpoints.BuscarVisitasEndpoint.as_view()),
    url(r'^api/regiones', endpoints.RegionesEndpoint.as_view()),
    url(r'^api/estados', endpoints.EstadosForRegionesEndpoint.as_view()),
    url(r'^api/municipios', endpoints.MunicipiosForEstadosEndpoint.as_view()),
    url(r'^api/distritos_electorales', endpoints.DistritoElectoralForEstadosEndpoint.as_view()),
    url(r'^api/cargos', endpoints.CargosForDependenciasEndpoint.as_view()),
    url(r'^api/dependencias', endpoints.DependenciasEndpoint.as_view()),
    url(r'^api/tipos_actividad', endpoints.TipoActividadEndpoint.as_view()),
    url(r'^api/clasificaciones', endpoints.ClasificacionEndpoint.as_view()),
    url(r'^api/medios', endpoints.MediosEndpoint.as_view()),
    url(r'^api/tipos_capitalizacion', endpoints.TipoCapitalizacionEndpoint.as_view()),
    url(r'^api/Inicio', endpoints.ReporteInicioEndpoint.as_view()),      
    )
