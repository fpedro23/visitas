from django import forms

from visitas_stg.models import *


__author__ = 'pedrocontreras'


class AddVisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = '__all__'

    def save(self, commit=True):
        instance = super(AddVisitaForm, self).save(commit=False)
        print self.changed_data

        if instance.identificador_unico is None:

            lista = Visita.objects.filter(dependencia__id=instance.dependencia.id).values(
                'identificador_unico').order_by('-identificador_unico')

            if lista.count() > 0:
                last_number = lista[0]
                numero = int(last_number.get('identificador_unico').split('_')[1]) + 1
                print numero
                string_id = '%s_%.3d' % (instance.dependencia.nombreDependencia.upper(), numero)
                string_id.upper()
                instance.identificador_unico = string_id
            else:
                numero = 1
                string_id = '%s_%.3d' % (instance.dependencia.nombreDependencia.upper(), numero)
                string_id.upper()
                instance.identificador_unico = string_id

        return super(AddVisitaForm, self).save(commit=commit)