from django.conf.urls import patterns, include, url
from django.contrib import admin

from visitas_stg import  views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'visitas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^busqueda-filtros/', views.buscar_visitas_web, name='consulta_filtros'),
    url(r'^visitas_stg/movimientos$', 'visitas_stg.views.movimientos', name='movimientos'),
    )
