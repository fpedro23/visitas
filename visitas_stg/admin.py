# coding=utf-8
from django.contrib import admin
from django.db.models import Q
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.contrib.auth.admin import UserAdmin

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

    def get_readonly_fields(self, request, obj=None):
        if request.user.userprofile.rol == 'US':
            return ('dependencia', )
        return super(VisitaAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        if request.user.userprofile.rol == 'US':
            qs = super(VisitaAdmin, self).get_queryset(request)
            return qs.filter(
                Q(dependencia__id=request.user.userprofile.dependencia.id)
            )

        return super(VisitaAdmin, self).get_queryset(request)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_dependencia', )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (('Personal info', ), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions', ), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates', ), {'fields': ('last_login', 'date_joined')}),
    )

    def get_dependencia(self, obj):
        return obj.userprofile.dependencia.nombreDependencia

    get_dependencia.short_description = 'Dependencia'


admin.site.register(Visita, VisitaAdmin)
admin.site.register(Region)
# admin.site.register(Estado)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Municipio)
admin.site.register(Cargo)
admin.site.register(Dependencia)
admin.site.register(TipoActividad)
admin.site.register(Clasificacion)
admin.site.register(CargoLocal)
admin.site.register(ParticipanteLocal)
admin.site.register(Medio)
admin.site.register(TipoCapitalizacion)
