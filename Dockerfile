# Usamos una imagen base de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Variables para usuario y grupo
ARG PUID=1000
ARG PGID=1000

# Crea el grupo y usuario con los IDs especificados
RUN groupadd -g ${PGID} appgroup && \
    useradd -u ${PUID} -g appgroup -m appuser

# Cambia el propietario del directorio de trabajo al nuevo usuario
RUN chown -R appuser:appgroup /app
# Copiamos el archivo de requisitos en el contenedor
COPY data/requirements.txt /app/requirements.txt
# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el proyecto al contenedor
COPY . /app

# Exponemos el puerto 80 si es necesario (si tu aplicación usa un servidor web, por ejemplo)
# EXPOSE 80

# Definimos el comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]
