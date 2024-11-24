# Prowlarr  

**Prowlarr** es un proyecto en desarrollo que tiene como objetivo automatizar la descarga de videos de YouTube y su integración con Sonarr. Actualmente se encuentra en una fase temprana, por lo que muchas características están en construcción o pendientes de ser implementadas. A pesar de esto, ya puedes usarlo para gestionar descargas de listas de reproducción y organizarlas según configuraciones específicas.  

## Estado del proyecto  

⚠️ Este proyecto está en desarrollo activo. Muchas funcionalidades todavía están incompletas o pueden cambiar en el futuro.  

¡Tu ayuda y retroalimentación son bienvenidas! Si deseas contribuir o reportar problemas, no dudes en abrir un *issue*.  

## Características  

- **Descarga de listas de reproducción**: Automatiza la descarga de videos desde YouTube usando `yt-dlp`.  
- **Integración avanzada con Sonarr**: Renombra, organiza y autoimporta los archivos descargados directamente a Sonarr mediante su API, asegurando una experiencia fluida y automatizada.  
- **Configuración flexible por serie**: Define idiomas de audio y subtítulos para cada lista de reproducción.  
- **Notificaciones por Telegram** *(opcional)*: Recibe alertas cuando se descargan nuevos episodios.  
- **Soporte Docker**: Fácil despliegue utilizando contenedores Docker.  


## Próximos pasos  

El proyecto está en constante evolución. Algunos de los objetivos para el futuro incluyen:  

- **Mejorar la integración con Sonarr**: Ampliar la funcionalidad para permitir la búsqueda y gestión de series directamente desde Sonarr.  
- **Incluir un buscador de YouTube**: Implementar un sistema que permita buscar y añadir listas de reproducción desde YouTube de forma más sencilla.  
- **Crear una interfaz gráfica (WebUI)**: Desarrollar una interfaz web para gestionar configuraciones, listas de reproducción y descargas de manera intuitiva.  


## Configuración  

### Archivo `series.yaml`  

El archivo `series.yaml` se utiliza para definir las listas de reproducción que deseas descargar y sus configuraciones específicas.  

Ejemplo:  

```yaml
series:
  - title: "Series Example"
    playlist:
      - "https://www.youtube.com/playlist_example"
      - "https://www.youtube.com/another_playlist"
    subtitles_language: "es,es,jp"
    audio_language: "es,en,ja"
```

### Variables de entorno

Las configuraciones generales se gestionan a través de las siguientes variables de entorno:

- `PGID`: ID del grupo para permisos en Docker.
- `PUID`: ID del usuario para permisos en Docker.
- `DOWNLOAD_INTERVAL`: Intervalo (en minutos) para buscar nuevos videos.
- `SONARR_API_IP`: Dirección IP del contenedor de Sonarr.
- `SONARR_API_PORT`: Puerto del API de Sonarr.
- `SONARR_API_KEY`: Clave de la API de Sonarr.
- `TELEGRAM_BOT_TOKEN` *(opcional)*: Token del bot de Telegram para notificaciones.
- `TELEGRAM_CHAT_ID` *(opcional)*: ID de chat de Telegram para enviar notificaciones.
- `SONARR_PATH`: Ruta única donde Sonarr detectará los episodios descargados.

## Uso

### Docker Compose

Ejemplo de configuración:

```yaml
services:
  plundarr:
    container_name: plundarr
    image: plundar
    environment:
      - PGID=1000
      - PUID=1000
      - DOWNLOAD_INTERVAL=60 # intervalo en minutos
      - SONARR_API_IP=SONARR_IP # dirección IP de Sonarr
      - SONARR_API_PORT=SONARR_PORT # puerto de Sonarr
      - SONARR_API_KEY=YOUR_SONARR_API_KEY # clave de API de Sonarr
      - TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN # (OPCIONAL) Token del bot de Telegram
      - TELEGRAM_CHAT_ID=YOUR_CHAT_ID # (OPCIONAL) ID de chat de Telegram
      - SONARR_PATH=YOUR_ROUTE_FROM_SONARR # ruta donde Sonarr detectará episodios
    volumes:
      - ${DOCKER_PATH}/plundarr:/app/config
      - ${HDD_PATH}/hdd3/downloads/plundarr:/downloads
```
## Créditos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Sonarr](https://sonarr.tv/)
- Inspirado por el deseo de automatizar y organizar contenido multimedia.


