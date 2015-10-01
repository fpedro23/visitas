# coding=utf-8
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from visitas_stg.models import *


# Register your models here.


class ParticipanteLocalInline(NestedStackedInline):
    model = ParticipanteLocal
    extra = 1


class CapitalizacionInline(NestedStackedInline):
    model = Capitalizacion
    extra = 1


class ActividadInLine(NestedStackedInline):
    model = Actividad
    extra = 1
    inlines = [ParticipanteLocalInline, CapitalizacionInline]
    fieldsets = [
        (None, {'fields': ['tipo_actividad', 'descripcion', 'clasificacion', 'problematica']}),

    ]


class VisitaAdmin(NestedModelAdmin):
    model = Visita
    inlines = [ActividadInLine]
    fieldsets = [
        (None, {'fields': ['dependencia']}),
        ('Información general', {'fields': ['fecha_visita', 'region', 'entidad', 'municipio', 'cargo', ]}),
    ]


admin.site.register(Visita, VisitaAdmin)
admin.site.register(Region)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Cargo)
admin.site.register(Dependencia)
admin.site.register(TipoActividad)
admin.site.register(Clasificacion)
admin.site.register(CargoLocal)
admin.site.register(ParticipanteLocal)
admin.site.register(Medio)
admin.site.register(TipoCapitalizacion)
