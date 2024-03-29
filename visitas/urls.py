from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from visitas_stg import views, endpoints
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'visitas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'visitas_stg.views.redirect_admin', name='redirect_admin'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
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
    url(r'^visitas/consulta_predefinidos$', 'visitas_stg.views.consulta_predifinidos', name='consulta_predifinidos'),
    url(r'^visitas/busqueda-filtros', views.buscar_visitas_web, name='consulta_filtros'),
    url(r'^visitas/register-by-token$',views.register_by_access_token),
    url(r'^visitas/listar-visitas', views.listar_visitas, name='listar_visitas'),
    url(r'^visitas/usuarios$', 'visitas_stg.views.usuarios', name='usuarios'),
    url('^visitas/ficha', views.fichaTecnica),
    url('^visitas/Predefinido_Estado', views.Predefinido_Estado),
    url('^visitas/Predefinido_Dependencia', views.Predefinido_Dependencia),
    url('^visitas/Predefinido_Region', views.Predefinido_Region),
    url('^visitas/Predefinido_Trece_Entidades', views.Predefinido_Trece_Entidades),


    url(r'^visitas/ayuda$', 'visitas_stg.views.ayuda', name='ayuda'),
    url(r'^visitas/videos$', 'visitas_stg.views.videos', name='videos'),
    url(r'^visitas/ver_video$', 'visitas_stg.views.ver_video', name='ver_video'),
    url(r'^visitas/manuales-Pdf$', 'visitas_stg.views.manualesPdf', name='manualesPdf'),


    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^api/ReportePP', endpoints.PptxReporteEndpoint.as_view()),
    url(r'^api/PptxVista', endpoints.PptxEndpoint.as_view()),
    url(r'^api/buscador', endpoints.BuscarVisitasEndpoint.as_view()),
    url(r'^api/regiones', endpoints.RegionesEndpoint.as_view()),
    url(r'^api/estados', endpoints.EstadosForRegionesEndpoint.as_view()),
    url(r'^api/municipios', endpoints.MunicipiosForEstadosEndpoint.as_view()),
    url(r'^api/distritos_electorales', endpoints.DistritoElectoralForEstadosEndpoint.as_view()),
    url(r'^api/cargos', endpoints.CargosForDependenciasEndpoint.as_view()),
    url(r'^api/cargo_nombre', endpoints.CargosForNombreEndpoint.as_view()),
    url(r'^api/dependencias', endpoints.DependenciasEndpoint.as_view()),
    url(r'^api/tipos_actividad', endpoints.TipoActividadEndpoint.as_view()),
    url(r'^api/clasificaciones', endpoints.ClasificacionEndpoint.as_view()),
    url(r'^api/medios', endpoints.MediosEndpoint.as_view()),
    url(r'^api/tipos_capitalizacion', endpoints.TipoCapitalizacionEndpoint.as_view()),
    url(r'^api/Inicio', endpoints.ReporteInicioEndpoint.as_view()),
    url(r'^api/reporte_estado_id', endpoints.ReporteEstadoEndpoint.as_view()),
    url(r'^api/reporte_dependencia_id', endpoints.ReporteDependenciaEndpoint.as_view()),
    url(r'^api/reporte_estado', endpoints.ReporteEstadosEndpoint.as_view()),
    url(r'^api/reporte_dependencia', endpoints.ReporteDependenciasEndpoint.as_view()),
    url(r'^api/reporte_region', endpoints.ReporteRegionEndpoint.as_view()),
    url(r'^api/id_unico', endpoints.IdUnicoEndpoint.as_view()),
    url(r'^api/reporte_inicio', endpoints.ReporteInicioEndpoint.as_view()),

    url(r'^ico_SISEF.ico/$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'ico_SISEF.ico'))

)
