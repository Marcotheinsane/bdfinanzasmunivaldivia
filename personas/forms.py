from django import forms
from django.core.exceptions import ValidationError
from .models import Persona


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'rut', 'organizacion', 'fono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'autofocus': True
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9',
            }),
            'organizacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organización (opcional)',
            }),
            'fono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono (opcional)',
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'rut': 'RUT',
            'organizacion': 'Organización',
            'fono': 'Teléfono',
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            raise ValidationError('El RUT es obligatorio')
        
        # Normalizar RUT (eliminar puntos)
        rut_limpio = rut.replace('.', '').upper()
        
        # Validar que no exista otro registro con este RUT
        queryset = Persona.objects.filter(rut__iexact=rut_limpio)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise ValidationError('El RUT ya existe en el sistema')
        
        return rut_limpio

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or not nombre.strip():
            raise ValidationError('El nombre es obligatorio')
        return nombre.strip()


class ImportarCSVForm(forms.Form):
    archivo = forms.FileField(
        label='Seleccionar archivo CSV',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv',
        }),
        help_text='Formato: nombre,rut,organizacion,fono'
    )
