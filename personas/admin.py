from django.contrib import admin
from .models import Persona


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'organizacion', 'fono', 'fecha_creacion')
    search_fields = ('nombre', 'rut')
    list_filter = ('fecha_creacion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
