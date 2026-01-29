# Despliegue en Google Cloud Run

## Prerequisitos

1. **Cuenta Google Cloud** - [Crear cuenta](https://cloud.google.com/free)
2. **Google Cloud SDK** instalado - [Instrucciones](https://cloud.google.com/sdk/docs/install)
3. **Docker** instalado en tu máquina local
4. **PostgreSQL** ya deployado (Cloud SQL) o usar SQLite

## Configuración inicial

```bash
# 1. Autenticarse en Google Cloud
gcloud auth login

# 2. Crear un proyecto (o usar uno existente)
gcloud projects create personas-app-bdmuni --display-name "Personas App"
gcloud config set project personas-app-bdmuni

# 3. Habilitar APIs necesarias
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable sqladmin.googleapis.com  # Solo si usas Cloud SQL
```

## Opción 1: Deploy manual desde terminal (Más rápido)

```bash
# Desde la carpeta de la app
cd personas_app

# 1. Autenticarse en Docker (una sola vez)
gcloud auth configure-docker

# 2. Build de la imagen
docker build -t gcr.io/personas-app-bdmuni/personas-app:latest .

# 3. Push a Container Registry
docker push gcr.io/personas-app-bdmuni/personas-app:latest

# 4. Deploy a Cloud Run
gcloud run deploy personas-app \
  --image gcr.io/personas-app-bdmuni/personas-app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60 \
  --set-env-vars="DEBUG=False,DATABASE_URL=YOUR_DATABASE_URL"
```

## Opción 2: Usar GitHub Actions para CI/CD automático

Crea archivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Auth to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_CREDENTIALS }}
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy personas-app \
            --source . \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated
```

Luego:
1. Ve a Google Cloud Console
2. En Settings → Secrets, agrega `GCP_CREDENTIALS` con tu JSON de la cuenta de servicio

## Configurar Base de Datos

### Opción A: Cloud SQL (PostgreSQL)

```bash
# 1. Crear instancia
gcloud sql instances create personas-db \
  --database-version POSTGRES_15 \
  --tier db-f1-micro \
  --region us-central1

# 2. Crear base de datos
gcloud sql databases create personas \
  --instance personas-db

# 3. Crear usuario
gcloud sql users create postgres \
  --instance personas-db \
  --password=TU_CONTRASEÑA_SEGURA

# 4. Obtener CONNECTION_NAME
gcloud sql instances describe personas-db \
  --format="value(connectionName)"

# Actualizar variable de entorno en Cloud Run:
DATABASE_URL=postgresql://postgres:PASSWORD@/personas?host=/cloudsql/PROJECT:REGION:INSTANCE_NAME
```

### Opción B: SQLite (Más fácil, pero solo local)

Ya está configurado. La app usa `db.sqlite3` localmente.

## Variables de entorno necesarias

En Cloud Run, configura estas variables:

```
DEBUG = False
ALLOWED_HOSTS = tu-app.run.app
SECRET_KEY = tu-secret-key-segura-y-larga
DATABASE_URL = postgresql://user:password@host/dbname  # Si usas PostgreSQL
```

## Ver logs de la app

```bash
gcloud run logs read personas-app --region us-central1 --limit 50
```

## Limpiar recursos

```bash
# Eliminar Cloud Run service
gcloud run services delete personas-app --region us-central1

# Eliminar imagen de Container Registry
gcloud container images delete gcr.io/personas-app-bdmuni/personas-app

# Eliminar base de datos Cloud SQL (si aplica)
gcloud sql instances delete personas-db
```

## Notas importantes

- **Puerto**: Cloud Run requiere puerto `8080` (configurado en el Dockerfile)
- **Timeout**: Máximo 60 minutos, por defecto 5 minutos
- **Memoria**: Mínimo 128Mi, máximo 8Gi (comienza con 512Mi)
- **Costo**: 2 millones de requests/mes gratis, 360k segundos de CPU/mes gratis

## Troubleshooting

```bash
# Ver detalles del servicio
gcloud run services describe personas-app --region us-central1

# Ver eventos recientes
gcloud run services describe personas-app --region us-central1 --format json

# Probar conexión a BD
gcloud cloud-sql-proxy personas-db --port=5432
```

¿Necesitas ayuda con algún paso específico?
