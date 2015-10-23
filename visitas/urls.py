from django.conf.urls import patterns, include, url
from django.contrib import admin
from visitas_stg import views, endpoints


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'visitas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^busqueda-filtros/', views.buscar_visitas_web, name='consulta_filtros'),

    url(r'^api/buscador', endpoints.BuscarVisitasEndpoint.as_view()),
    url(r'^api/regiones', endpoints.RegionesEndpoint.as_view()),
    url(r'^api/estados', endpoints.EstadosForRegionesEndpoint.as_view()),
    url(r'^api/municipios', endpoints.MunicipiosForEstadosEndpoint.as_view()),
    url(r'^api/distritos_electorales', endpoints.DistritoElectoralForEstadosEndpoint.as_view()),
    url(r'^api/cargos', endpoints.CargosForDependenciasEndpoint.as_view()),
    url(r'^api/nombres_cargos', endpoints.CargosForCargosEndpoint.as_view()),
    url(r'^api/dependencias', endpoints.DependenciasEndpoint.as_view()),
    url(r'^api/tipos_actividad', endpoints.TipoActividadEndpoint.as_view()),
    url(r'^api/clasificaciones', endpoints.ClasificacionEndpoint.as_view()),
    url(r'^api/medios', endpoints.MediosEndpoint.as_view()),
    url(r'^api/tipos_capitalizacion', endpoints.TipoCapitalizacionEndpoint.as_view()),
    url(r'^api/reporte_inicio', endpoints.ReporteInicioEndpoint.as_view()),
    url(r'^api/reporte_estado', endpoints.ReporteEstadosEndpoint.as_view()),
)
