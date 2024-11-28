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
--
Para más configuraciones, visita la [documentación de configuración](plundar/doc/configuration.md).


## Créditos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Sonarr](https://sonarr.tv/)
- Inspirado por el deseo de automatizar y organizar contenido multimedia.


