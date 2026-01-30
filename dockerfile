FROM python:3.11-slim

# Configurar variables de entorno para Python y pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema (PostgreSQL client, etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código de la app
COPY . .

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput --clear

# Render requiere escuchar en puerto 10000 (configurable via PORT)
EXPOSE 10000

# Crear usuario no-root para seguridad
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando para correr Gunicorn en Render
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-10000}", "--workers", "3", "--worker-class", "sync", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "personas_app.wsgi:application"]
