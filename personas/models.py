from django.db import models
from django.core.exceptions import ValidationError


def validar_rut(value):
    """Valida formato básico de RUT chileno"""
    import re
    # Acepta formatos: 12345678-9 o 123456789
    if not re.match(r'^\d{1,8}-?\d$', value.replace('.', '')):
        raise ValidationError('RUT debe tener formato válido (ej: 12345678-9)')


class Persona(models.Model):
    nombre = models.CharField(max_length=100, help_text='Nombre completo')
    rut = models.CharField(
        max_length=12,
        unique=True,
        help_text='RUT sin puntos (ej: 12345678-9)',
        validators=[validar_rut]
    )
    organizacion = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text='Organización o institución'
    )
    fono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text='Teléfono de contacto'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f'{self.nombre} ({self.rut})'
