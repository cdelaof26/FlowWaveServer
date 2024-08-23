# FlowWave Server

### Descripción
Esta serie de scripts forman un servidor para la transferencia de 
ficheros a través de WebSockets.


### Copyright
<pre>
https://github.com/cdelaof26
</pre>

Por el momento, este software no contiene una licencia, por
lo que todos los derechos están reservados - cdelaof26.


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
</pre>


### Configuración
Al ejecutar por primera vez el servidor, se creará un archivo llamado `config`,
dentro de este es posible cambiar los parámetros mostrados en la tabla.

| Propiedad                 | Descripción                                                                                                 | Valores                      |
|---------------------------|-------------------------------------------------------------------------------------------------------------|------------------------------|
| `host_ip`                 | IP del servidor                                                                                             | `localhost`, `IPv4` o `URL`  |
| `port`                    | Puerto para la aplicación                                                                                   | Entero en rango `1024-49151` |
| `allow_shell_full_access` | Bandera que indica si el usuario puede ejecutar cualquier comando disponible (sin permisos administrativos) | `True` o `False`             |


### Historial de cambios

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
