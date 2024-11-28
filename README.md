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

## Configuración de Sonarr para integrarse con Plundarr

Para que la integración entre Sonarr y Plundarr funcione correctamente, es necesario configurar un perfil y un tag en Sonarr que Plundarr utilizará para identificar las series que debe descargar.

### Pasos para configurar Sonarr:

1. **Crear un perfil llamado "youtube"**:
   - Accede a la interfaz web de Sonarr.
   - Ve a **Settings** (Configuración).
   - En el menú lateral, selecciona **Profiles** (Perfiles).
   - Haz clic en **Add Profile** (Agregar perfil) y crea un perfil nuevo llamado "youtube".
   - Pon como Etiqueta (Tags) a este Profile "youtube".

2. **Asociar el tag "youtube" a las series**:
   - Cuando añadas una nueva serie en Sonarr y quieras que esta se descargue con Plundarr, asegúrate de asociarle el tag "youtube" que creaste anteriormente.
   - Este tag será utilizado por Plundarr para identificar qué series deben ser descargadas desde YouTube.

Una vez configurado esto, Plundarr podrá buscar todas las series con el tag "youtube" y comenzará el proceso de descarga automáticamente.

Recuerda que este tag es fundamental para que Plundarr funcione correctamente y reconozca las series que desea descargar desde YouTube.

## Agregar URL de Playlist para descarga

Cuando se inicia Plundarr por primera vez o cuando se agrega o borra una serie en Sonarr, Plundarr actualiza automáticamente el archivo `series.yaml`. Este archivo se encuentra en la configuración de Plundarr y contiene la información de las series y sus respectivas playlists.

### Estructura del archivo `series.yaml`:

El archivo `series.yaml` tiene la siguiente estructura básica:
```yaml
series:
  - title: "SeriesTitle"
    playlist:
      - ""
    subtitles_language: ""
    audio_language: ""
```
- **title**: El nombre de la serie que se ha agregado a Sonarr.
- **playlist**: La URL de la playlist de YouTube para la serie. Puedes añadir varias URLs de playlists dentro de este campo.
- **subtitles_language**: El idioma de los subtítulos para la serie (opcional).
- **audio_language**: El idioma de audio para la serie (opcional).

### Pasos para editar `series.yaml`:

1. **Ubicación del archivo**:
   - El archivo `series.yaml` se encuentra en la carpeta de configuración de Plundarr. Debes acceder a él para completar o modificar la información de las series.

2. **Rellenar los campos**:
   - Para cada serie, debes rellenar los campos correspondientes:
     - En **playlist**, agrega las URLs de las playlists de YouTube que deseas asociar a esa serie. Puedes incluir varias playlists bajo la clave `playlist`.
     - Los campos **subtitles_language** y **audio_language** son opcionales.
```yaml
series:
  - title: "TitleSerie"
    playlist:
      - "https://www.youtube.com/playlist?list=1234567"
      - "https://www.youtube.com/playlist?list=8901234"
    subtitles_language: "en"
    audio_language: "en"
  - title: "Another Series"
    playlist:
      - "https://www.youtube.com/playlist?list=1234567"
    subtitles_language: "es, en"
    audio_language: "es, en"
```
### Notas importantes:
- Puedes agregar tantas URLs de playlists como desees para cada serie bajo el campo `playlist`.
- Los campos `subtitles_language` y `audio_language` son opcionales, pero si los incluyes, asegúrate de usar los códigos de idioma correctos (por ejemplo, `en` para inglés, `es` para español).
- Una vez que hayas actualizado el archivo, Plundarr usará esta información para gestionar las descargas de los episodios asociados a las playlists de YouTube de las series.
- El archivo `series.yaml` se actualiza automáticamente cuando se inicia Plundarr por primera vez o cuando se agrega o elimina una serie en Sonarr.

### Funcionamiento de Plundarr

Una vez configurado correctamente el archivo `series.yaml`, Plundarr comenzará a descargar los videos de las playlists de YouTube de manera recursiva. A medida que nuevos videos aparezcan en las playlists configuradas, Plundarr los descargará automáticamente.

Cuando la descarga de un episodio termine, Plundarr pedirá a Sonarr que importe el archivo al directorio correspondiente en su sistema. De esta forma, los episodios se añadirán automáticamente a Sonarr para su gestión.

Además, cuando una serie sea eliminada de Sonarr, Plundarr eliminará automáticamente esa serie del archivo `series.yaml`, manteniendo así la sincronización entre Sonarr y Plundarr.

### Comportamiento de descarga de Plundarr

Plundarr solo descargará los videos de las playlists que aún no han sido descargados previamente. Para que un video sea descargado, debe cumplir con las siguientes condiciones:

1. **La serie debe estar siendo monitorizada por Sonarr.**
2. **El video no debe estar marcado como importado en Sonarr.**

Si Sonarr no está monitorizando una serie o si ya tiene ese video descargado e importado, Plundarr no volverá a descargarlo. Plundarr revisa las playlists de YouTube de forma recursiva, pero solo descargará aquellos episodios que aún no han sido descargados y que cumplen con los requisitos anteriores.

Esto asegura que Plundarr solo gestione la descarga de los episodios que Sonarr aún no ha importado y que están pendientes de ser procesados.

### Mejora de la conectividad con Sonarr a través del Webhook

Plundarr incluye un webhook que se puede conectar con Sonarr para mejorar la sincronización y la gestión de las series. Para configurar esta conectividad, deberás apuntar a la URL `http://plundarr:3737/api` y configurar el usuario y contraseña que hayas seleccionado en la configuración de Plundarr.

Una vez configurado, Sonarr podrá enviar las siguientes notificaciones a Plundarr:

- **Serie Agregada**: Cuando una serie se agrega a Sonarr, Plundarr creará la sección correspondiente en el archivo `series.yaml`.
- **Serie Borrada**: Si una serie es eliminada de Sonarr, Plundarr eliminará esa serie de su archivo `series.yaml`.
- **Episodio Borrado**: Si un episodio de una serie es borrado, Plundarr eliminará ese episodio de la lista de descargados.

Este webhook mejora la automatización entre Sonarr y Plundarr, asegurando que ambas aplicaciones mantengan su sincronización y que los archivos descargados sean gestionados correctamente.


## Descargar Series

Plundarr se comunica de forma activa con Sonarr para saber que series necesita buscar, para ello es necesario colocar un 'tag' en Sonarr que nos confirme que esa serie es de youtube para 

## Créditos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Sonarr](https://sonarr.tv/)
- Inspirado por el deseo de automatizar y organizar contenido multimedia.
