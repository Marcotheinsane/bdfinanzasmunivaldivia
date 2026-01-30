# Deployment a Render + Supabase

## Paso 1: Preparar Base de Datos en Supabase

1. Ve a [supabase.com](https://supabase.com)
2. Crea un nuevo proyecto
3. Copia la connection string en el formato PostgreSQL:
   ```
   postgresql://postgres:password@db.supabase.co:5432/postgres?sslmode=require
   ```

## Paso 2: Preparar el Repositorio

1. Inicializa Git:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Crea un repositorio en GitHub/GitLab/Gitea

3. Sube tu código:
   ```bash
   git remote add origin <tu-repo-url>
   git branch -M main
   git push -u origin main
   ```

## Paso 3: Deploy en Render

1. Ve a [render.com](https://render.com) y regístrate/inicia sesión

2. Crea un nuevo servicio web (New > Web Service)

3. Conecta tu repositorio de GitHub

4. Configuración:
   - **Name**: personas-app
   - **Environment**: Python 3
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```
     gunicorn --bind 0.0.0.0:${PORT} --workers 3 --worker-class sync --timeout 120 personas_app.wsgi:application
     ```

## Paso 4: Variables de Entorno en Render

En la sección de "Environment Variables", añade:

```
SECRET_KEY=<genera-una-key-segura>
DEBUG=False
RENDER=true
ALLOWED_HOSTS=<tu-app-name>.onrender.com
DATABASE_URL=postgresql://postgres:password@db.supabase.co:5432/postgres?sslmode=require
```

## Paso 5: Inicializar Base de Datos

Una vez deployado, ejecuta las migraciones:

```bash
# En la consola de Render (Dashboard > Services > Shell)
python manage.py migrate
```

## Notas Importantes

- El `requirements.txt` ya incluye `psycopg[binary]` para PostgreSQL
- `whitenoise` maneja los archivos estáticos sin necesidad de CDN
- El puerto es automáticamente asignado por Render (variable $PORT)
- Las conexiones SSL se requieren para Supabase (sslmode=require)
- Los archivos estáticos se recopilan automáticamente en el build

## Troubleshooting

- **Error de migraciones**: Verifica que `DATABASE_URL` sea correcta
- **Static files no cargan**: Ejecuta `python manage.py collectstatic` manualmente
- **Conexión a BD rechazada**: Verifica que las credenciales de Supabase sean correctas
