#!/usr/bin/env python
"""
Script de inicialización de la aplicación
Crea la base de datos y realiza las migraciones
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personas_app.settings")
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.core.management import execute_from_command_line

print("=" * 60)
print("Inicializando aplicación de Registro de Personas")
print("=" * 60)

# Crear migraciones iniciales
print("\n1. Creando migraciones...")
execute_from_command_line(['manage.py', 'makemigrations', 'personas'])

# Aplicar migraciones
print("\n2. Aplicando migraciones...")
execute_from_command_line(['manage.py', 'migrate'])

print("\n" + "=" * 60)
print(" Inicialización completada exitosamente")
print("=" * 60)
print("\nPara ejecutar la aplicación:")
print("  python manage.py runserver")
print("\nLa app estará disponible en:")
print("  http://127.0.0.1:8000/")
print("\nPara importar el archivo de ejemplo:")
print("  1. Abre la app en tu navegador")
print("  2. Click en '📥 Importar CSV'")
print("  3. Selecciona 'ejemplo_personas.csv'")
print("=" * 60)
