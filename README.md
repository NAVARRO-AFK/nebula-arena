# Nebula Arena: infraestructura y despliegue de videojuegos en la nube

Proyecto integrador de la Unidad 3. Un servidor de partida multijugador desplegado con Kubernetes y Agones, con pipeline CI/CD, autoescalado guiado por métricas, prueba de carga con Locust, tabla de líderes serverless e infraestructura declarada con Terraform.

## Estructura

- `server/`: servidor de partida (WebSocket), pruebas y Dockerfile.
- `k8s/`: flota de Agones, autoescalador y monitor de Prometheus.
- `infra/`: Terraform que declara Agones, la flota y el autoescalador.
- `serverless/`: tabla de líderes en Flask y SQLite (sustituto local de Cloud Run).
- `loadtest/`: pruebas de carga con Locust y script de graficado.
- `.github/workflows/`: pipeline de pruebas y publicación de imagen en ghcr.io.

## Entorno

Desarrollado en una Mac con kind (Kubernetes local), sin cuenta de Google Cloud ni AWS. Las limitaciones de este entorno se explican en el reporte técnico.
