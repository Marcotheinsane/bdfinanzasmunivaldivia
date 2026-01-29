import csv
from io import TextIOWrapper
import unicodedata
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Persona
from .forms import PersonaForm, ImportarCSVForm


def normalizar(texto):
    """Normaliza texto removiendo acentos y convirtiendo a minúsculas"""
    texto = texto.strip().lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


def verificar_logo_existe():
    """Verifica si existe el logo en la carpeta de estáticos"""
    logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png')
    return os.path.exists(logo_path)


def obtener_contexto_base():
    """Retorna el contexto base para todos los templates"""
    return {'logo_exists': verificar_logo_existe()}


def lista_personas(request):
    """Muestra la lista completa de personas"""
    personas = Persona.objects.all()
    contexto = obtener_contexto_base()
    contexto.update({
        'personas': personas,
        'total': personas.count(),
    })
    return render(request, 'personas/lista.html', contexto)


def agregar_persona(request):
    """Agrega una nueva persona"""
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Persona {form.cleaned_data['nombre']} agregada correctamente")
                return redirect('lista_personas')
            except IntegrityError:
                messages.error(request, 'El RUT ya existe en el sistema')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PersonaForm()
    
    contexto = obtener_contexto_base()
    contexto.update({'form': form, 'accion': 'Agregar'})
    return render(request, 'personas/formulario.html', contexto)


def editar_persona(request, id):
    """Edita una persona existente"""
    persona = get_object_or_404(Persona, pk=id)
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Persona {form.cleaned_data['nombre']} actualizada correctamente")
                return redirect('lista_personas')
            except IntegrityError:
                messages.error(request, 'El RUT ya existe en el sistema')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PersonaForm(instance=persona)
    
    contexto = obtener_contexto_base()
    contexto.update({'form': form, 'accion': 'Editar', 'persona': persona})
    return render(request, 'personas/formulario.html', contexto)


def eliminar_persona(request, id):
    """Elimina una persona"""
    persona = get_object_or_404(Persona, pk=id)
    
    if request.method == 'POST':
        nombre = persona.nombre
        persona.delete()
        messages.success(request, f"Persona {nombre} eliminada correctamente")
        return redirect('lista_personas')
    
    contexto = obtener_contexto_base()
    contexto.update({'persona': persona})
    return render(request, 'personas/confirmar_eliminar.html', contexto)

def importar_csv(request):
    """Importa personas desde un archivo CSV"""
    if request.method == 'POST':
        form = ImportarCSVForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                archivo = request.FILES['archivo']

                # Leer todo el archivo UNA sola vez
                contenido = archivo.read().decode('latin-1')

                from io import StringIO
                data = StringIO(contenido)

                # CSV real usa ;
                reader = csv.reader(data, delimiter=';')

                # en este caso se salta el encabezado para no procesarlo y asi no leer dos veces el archivo
                next(reader, None)

                cantidad_exitosas = 0
                cantidad_errores = 0
                errores_detalle = []

                for fila in reader:
                    try:
                        if len(fila) < 4:
                            cantidad_errores += 1
                            errores_detalle.append('Fila incompleta')
                            continue

                        nombre = fila[0].strip()
                        rut = fila[1].strip().replace('.', '').upper()
                        organizacion = fila[2].strip() or None
                        fono = fila[3].strip() or None

                        if not nombre or not rut:
                            cantidad_errores += 1
                            errores_detalle.append('Nombre o RUT vacío')
                            continue

                        if Persona.objects.filter(rut__iexact=rut).exists():
                            cantidad_errores += 1
                            errores_detalle.append(f'RUT {rut} ya existe')
                            continue

                        Persona.objects.create(
                            nombre=nombre,
                            rut=rut,
                            organizacion=organizacion,
                            fono=fono
                        )

                        cantidad_exitosas += 1

                    except Exception as e:
                        cantidad_errores += 1
                        errores_detalle.append(str(e))

                if cantidad_exitosas:
                    messages.success(
                        request,
                        f'{cantidad_exitosas} persona(s) importada(s) correctamente'
                    )
                if cantidad_errores:
                    messages.warning(
                        request,
                        f'{cantidad_errores} error(es) durante la importación'
                    )

                return redirect('lista_personas')

            except Exception as e:
                messages.error(request, f'Error al procesar CSV: {e}')
                return redirect('lista_personas')

    else:
        form = ImportarCSVForm()

    return render(request, 'personas/importar_csv.html', {'form': form})
