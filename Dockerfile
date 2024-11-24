# Usamos una imagen base de Python
FROM python:3.13-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Variables para usuario y grupo
ARG PUID=1000
ARG PGID=1000

# Instalamos dependencias del sistema necesarias, incluyendo ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


# Crea el grupo y usuario con los IDs especificados
RUN groupadd -g ${PGID} appgroup && \
    useradd -u ${PUID} -g appgroup -m appuser

# Copiamos el archivo de requisitos en el contenedor
COPY src/data/requirements.txt /app/requirements.txt

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el proyecto al contenedor
COPY src/. /app

# Cambia el propietario de los directorios de datos y configuración a appuser
RUN chown -R appuser:appgroup /app /app/data /app/config

# Cambiar al usuario normal (no root) para la ejecución del contenedor
USER appuser

# Exponemos el puerto 80 si es necesario (si tu aplicación usa un servidor web, por ejemplo)
# EXPOSE 80

# Definimos el comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]
