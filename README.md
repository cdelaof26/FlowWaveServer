# FlowWave Server

### Descripción
Esta serie de scripts forman un servidor para la transferencia de 
ficheros a través de WebSockets principalmente por redes locales.


### Copyright
<pre>
MIT License

Copyright (c) 2024 cdelaof26

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
</pre>

**Antes de usar este software, revisa [LICENSE (full document)](LICENSE).**

La licencia del MIT solo aplica a la versión `v0.0.3` y posteriores de 
FlowWave Server.


### Dependencias
Para el desarrollo se requiere de lo siguiente:
- Python 3.9 ó más reciente
- Librería `websockets`


### Uso
<pre>
# Clonar el repositorio
$ git clone https://github.com/cdelaof26/FlowWaveServer.git

# Ingresar a la carpeta
$ cd FlowWaveServer

# Instalar dependencias
$ python -m pip install -r requirements.txt 

# Ejecutar el servidor en puerto 6789
$ python server.py

# Ejecutar el servidor y visualizar cliente
#   La página web (cliente) será visible en localhost:80
$ python http_server.py
</pre>

**Notas**: 
- Al utilizar `http_server.py`, se requiere que el [frontend](https://github.com/cdelaof26/FlowWave)
  se encuentre en el mismo directorio padre que la carpeta de este proyecto y 
  tenga por nombre `FlowWave`.
- Se puede cambiar el puerto sobre el cual se muestra el cliente al editar 
  `http_server.py`.
- Si se desea acceder desde otro dispositivo al cliente utilizando `http_server.py`,
  se debe colocar la IP del servidor en el navegador del otro.


### Configuración
Al ejecutar por primera vez el servidor, se creará un archivo llamado `config`,
dentro de este es posible cambiar los parámetros mostrados en la tabla.

| Propiedad                 | Descripción                                                                                     | Valores                      |
|---------------------------|-------------------------------------------------------------------------------------------------|------------------------------|
| `host_ip`                 | IP del servidor                                                                                 | `localhost`, `IPv4` o `URL`  |
| `port`                    | Puerto para la aplicación                                                                       | Entero en rango `1024-49151` |
| `allow_shell_full_access` | Indica si el usuario puede ejecutar cualquier comando disponible (sin permisos administrativos) | `True` o `False`             |
| `allow_download_files`    | Indica si el usuario puede descargar archivos del servidor                                      | `True` o `False`             |
| `allow_upload_files`      | Indica si el usuario puede subir archivos al servidor                                           | `True` o `False`             |

**Nota**: Aunque se coloque `allow_shell_full_access` en `True`, este no es 
completamente interactivo, lo que se traduce en que comandos que requieren de un 
flujo constante de datos no serán utilizables (por ejemplo `less`, `nano`, `python` 
[modo interactivo], etc).


### Historial de cambios

#### v0.0.3_1
- Resuelve problema al descargar archivos
- Resuelve problema en el cual el server se cae al ingresar una cadena vacía
- Resuelve problemas de compatibilidad con ciertos caracteres en la respuesta

#### v0.0.3
- Agregado `http_server.py`: servidor básico para mostrar el cliente
- Implementado subir y descargar archivos
  - Implementados permisos para subir y descargar archivos

#### v0.0.2
- Agregado archivo de configuración
- Ya no es posible cambiar el puerto de la aplicación por medio de línea de comando
- Se implementan validaciones sobre los comandos para evitar ejecución de código 
  malicioso en el modo restringido
- Mensaje `Comando desconocido` cambiado por `Invalid command`

#### v0.0.1_1
- Agregado archivo de dependencias
- Mensaje `Unknown command` cambiado por `Comando desconocido`

#### v0.0.1
- Proyecto inicial
