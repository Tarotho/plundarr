# **Configuración de la Aplicación**

Este archivo detalla las configuraciones necesarias para usar la aplicación correctamente. Todas las configuraciones se manejan a través de **variables de entorno**, que deben definirse al ejecutar el contenedor Docker.

---

## **Variables de Entorno**

### **Configuraciones Opcionales**

#### **Configuraciones Básicas**

- **`PGID`**: ID del grupo para permisos en Docker.  
  Ejemplo: `1000`

- **`PUID`**: ID del usuario para permisos en Docker.  
  Ejemplo: `1000`

- **`DOWNLOAD_INTERVAL`**: Intervalo de tiempo (en minutos) para buscar y descargar nuevos videos.  
  Ejemplo: `60`

#### **Seguridad con Sonarr (Opcional)**

- **`PLUNDARR_KEY`**: Clave personalizada para autenticar solicitudes a la API de Sonarr.  
  Ejemplo: `supersecurekey123`

- **`PLUNDARR_USER`**: Usuario para autenticar la conexión con Sonarr.  
  Ejemplo: `admin`

#### **Telegram (Opcional)**

- **`TELEGRAM_BOT_TOKEN`**: Token del bot de Telegram para enviar notificaciones.  
  Ejemplo: `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ`

- **`TELEGRAM_CHAT_ID`**: ID del chat de Telegram donde se enviarán las notificaciones.  
  Ejemplo: `987654321`

### **Configuraciones Obligatorias**

#### **Sonarr**

- **`SONARR_API_IP`**: Dirección IP donde está corriendo la API de Sonarr.  
  Ejemplo: `192.168.1.100`

- **`SONARR_API_PORT`**: Puerto usado por la API de Sonarr.  
  Ejemplo: `8989`

- **`SONARR_API_KEY`**: Clave de la API de Sonarr para autenticar las solicitudes.  
  Ejemplo: `abcd1234efgh5678`

- **`SONARR_PATH`**: Ruta donde Sonarr detectará los episodios descargados.  
  Ejemplo: `/downloads`

---

### 1. **Docker Compose**  
Agrega las variables en el archivo `docker-compose.yml` bajo la sección `environment`. Ejemplo:

```yaml
services:
  app:
    image: tarotho/plundarr:latest
    environment:
      - PGID: 1000
      - PUID: 1000
      - DOWNLOAD_INTERVAL: 60
      - SONARR_API_IP: 192.168.1.100
      - SONARR_API_PORT: 8989
      - SONARR_API_KEY: abcd1234efgh5678
      - SONARR_PATH: /downloads
      - PLUNDARR_KEY: supersecurekey123
      - PLUNDARR_USER: admin
      - TELEGRAM_BOT_TOKEN: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ
      - TELEGRAM_CHAT_ID: 987654321
      - PLUNDARR_KEY=123456
      - PLUNDARR_USER=PlundarUser
    volumes:
      - /path/to/your/docker/config/plundarr:/app/config
      - /path/to/your/downloads/plundarr:/plundarr
    networks:
      - arr

sonarr:
    image: linuxserver/sonarr:latest
    container_name: sonarr
    restart: no
    ports:
      - 8989:8989
    environment:
      - PGID=${PGID}
      - PUID=${PUID}
      - TZ=Europe/Madrid
    volumes:
      - /path/to/your/docker/config/sonarr:/config
      - /path/to/your/media:/media
      - /path/to/your/downloads:/downloads
      - /path/to/your/downloads/plundarr:/plundarr  # Esta línea conecta la carpeta de Plundarr con Sonarr
    networks:
      - arr

networks:
  arr:
    driver: bridge  # Usamos la red 'bridge' de Docker para asegurar la comunicación entre contenedores
```
## Contenedor de Sonarr

El siguiente bloque de configuración es para el contenedor de `Sonarr`. Aquí es donde se hace referencia a la ruta de `plundarr` a través de la variable `SONARR_PATH`, de este modo enseñamos a Sonarr donde están los archivos descargados con Plundar.

- **Variable `SONARR_PATH`**: En el contenedor de Sonarr, debes asegurarte de que la ruta donde Sonarr busca los episodios descargados coincida con la ruta que `Plundarr` utiliza para almacenarlos. Esto se logra mediante el siguiente volumen:
```yaml
  - /path/to/your/downloads/plundarr:/plundarr
```
  Esto garantiza que los archivos descargados por `Plundarr` estén disponibles para que Sonarr los gestione.

##Configuracion del Network

No olvidar incluir la network de tipo bridge para que se comuniquen correctamente ambos contenedores.


### 2. **Variables de Entorno Manualmente**  
Si no usas Docker Compose, define las variables directamente al ejecutar Docker:

```bash
docker run -d \
  --name mi-aplicacion \
  -e PGID=1000 \
  -e PUID=1000 \
  -e DOWNLOAD_INTERVAL=60 \
  -e SONARR_API_IP=192.168.1.100 \
  -e SONARR_API_PORT=8989 \
  -e SONARR_API_KEY=abcd1234efgh5678 \
  -e SONARR_PATH=/downloads \
  -e PLUNDARR_KEY=supersecurekey123 \
  -e PLUNDARR_USER=admin \
  -e TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ \
  -e TELEGRAM_CHAT_ID=987654321 \
  --volume /path/to/your/docker/config/plundarr:/app/config \
  --volume /path/to/your/downloads/plundarr:/plundarr \
  --network arr \
  taro/plundarr:latest
```

---

## **Notas**

- Asegúrate de mantener las variables **`PLUNDARR_KEY`** y **`PLUNDARR_USER`** seguras para evitar accesos no autorizados.
- Los valores de **`PGID`** y **`PUID`** deben coincidir con los permisos de los volúmenes en tu sistema host.
- Para una mejor seguridad, no incluyas las claves sensibles directamente en el archivo `docker-compose.yml` o en otros archivos visibles. Utiliza herramientas como **Docker Secrets** o un archivo `.env` para mantener estas claves de forma más segura.
- **`TELEGRAM_BOT_TOKEN`** y **`TELEGRAM_CHAT_ID`** son opcionales, pero te permitirán recibir notificaciones sobre el estado de las descargas.
- Si usas **Sonarr** y **Plundarr** en contenedores separados, asegúrate de que el contenedor de tu aplicación pueda comunicarse con la API de **Sonarr** mediante las variables `SONARR_API_IP`, `SONARR_API_PORT`, y `SONARR_API_KEY`.

