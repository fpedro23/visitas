# coding=utf-8
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

import views
from visitas_stg.models import *



# Register your models here.


class ProblematicaSocialInLine(NestedStackedInline):
    model = ProblematicaSocial
    extra = 1

class ParticipanteLocalInline(NestedStackedInline):
    model = ParticipanteLocal
    extra = 1


class CapitalizacionInline(NestedStackedInline):
    model = Capitalizacion
    extra = 1


class ActividadInLine(NestedStackedInline):
    model = Actividad
    extra = 1
    inlines = [ParticipanteLocalInline, CapitalizacionInline, ProblematicaSocialInLine]
    fieldsets = [
        (None, {'fields': ['tipo_actividad', 'descripcion', 'clasificacion', ]}),

    ]


class VisitaAdmin(NestedModelAdmin):
    model = Visita
    inlines = [ActividadInLine]
    fieldsets = [
        ('Información básica de la visita', {'fields': ['dependencia', 'fecha_visita',]}),
        ('Localización', {'fields': ['region', 'entidad', 'municipio', ]}),
        ('Datos electorales', {'fields': ['distrito_electoral', 'partido_gobernante',]}),
        ('Funcionarios', {'fields': ['cargo', ]}),

    ]


admin.site.register(Visita, VisitaAdmin)
admin.site.register(Region)
# admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Cargo)
admin.site.register(Dependencia)
admin.site.register(TipoActividad)
admin.site.register(Clasificacion)
admin.site.register(CargoLocal)
admin.site.register(ParticipanteLocal)
admin.site.register(Medio)
admin.site.register(TipoCapitalizacion)
