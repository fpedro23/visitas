# coding=utf-8
from django.contrib import admin
from django.db.models import Q
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.contrib.auth.admin import UserAdmin

from visitas_stg.forms import AddVisitaForm
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
    form = AddVisitaForm
    list_display = (
    '__str__', 'identificador_unico', 'dependencia', 'region', 'entidad', 'municipio', 'cargo', 'partido_gobernante',
    'distrito_electoral', )

    fieldsets = [
        ('Información básica de la visita', {'fields': ['identificador_unico', 'dependencia', 'fecha_visita', ]}),
        ('Localización', {'fields': ['region', 'entidad', 'municipio', ]}),
        ('Datos electorales', {'fields': ['distrito_electoral', 'partido_gobernante', ]}),
        ('Funcionarios', {'fields': ['cargo', ]}),

    ]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('identificador_unico',)
        return readonly_fields

    def get_queryset(self, request):
        if request.user.userprofile.rol == 'US':
            qs = super(VisitaAdmin, self).get_queryset(request)
            return qs.filter(
                Q(dependencia__id=request.user.userprofile.dependencia.id)
            )

        return super(VisitaAdmin, self).get_queryset(request)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        if request.user.userprofile.rol == 'US':
            if db_field.name == "dependencia":
                kwargs["queryset"] = Dependencia.objects.filter(id=request.user.userprofile.dependencia.id)

            if db_field.name == "cargo":
                kwargs["queryset"] = Cargo.objects.filter(dependencia__id=request.user.userprofile.dependencia.id)

        return super(VisitaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_dependencia', 'get_rol', )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (('Personal info', ), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions', ), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates', ), {'fields': ('last_login', 'date_joined')}),
    )

    def f(self, x):
        return {
            'US': 'Usuario de dependencia',
            'AD': 'Administrador General',
        }.get(x, 'Sin Rol Asignado')

    def get_rol(self, obj):
        try:
            nombre_rol = self.f(obj.userprofile.rol)
            return nombre_rol
        except Exception as e:
            print e
            nombre = ''
            return nombre

    get_rol.short_description = 'Rol de usuario'


    def get_dependencia(self, obj):
        try:
            nombre_dependencia = obj.userprofile.dependencia.nombreDependencia
            return nombre_dependencia
        except Exception as e:
            print e
            nombre_dependencia = 'Sin dependencia asignada'
            return nombre_dependencia

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
admin.site.register(ParticipanteLocal)
admin.site.register(DistritoElectoral)
admin.site.register(Medio)
admin.site.register(TipoCapitalizacion)
admin.site.register(PartidoGobernante)
