from django.conf.urls import patterns, include, url
from django.contrib import admin

from visitas_stg import  views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'visitas_stg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^busqueda-filtros/', views.buscar_visitas_web, name='consulta_filtros'),
    url(r'^visitas/catalogos$', 'visitas_stg.views.catalogos', name='catalogos'),
    url(r'^visitas/catalogo-funcionarios$', 'visitas_stg.views.catalogo_funcionarios', name='catalogo_funcionarios'),
    url(r'^visitas/catalogo-medios$', 'visitas_stg.views.catalogo_medios', name='catalogo_medios'),
    url(r'^visitas/catalogo-tipoActividad$', 'visitas_stg.views.catalogo_tipoActividad', name='catalogo_tipoActividad'),
    url(r'^visitas/catalogo-capitalizacion$', 'visitas_stg.views.catalogo_capitalizacion', name='catalogo_capitalizacion'),
    url(r'^visitas/consultas$', 'visitas_stg.views.consultas', name='consultas'),
    url(r'^visitas/consulta_filtros$', 'visitas_stg.views.consulta_filtros', name='consulta_filtros'),
    )
