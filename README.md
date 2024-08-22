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

# Ejecutar el servidor en puerto 8080
$ python server.py 8080
</pre>


### Historial de cambios

#### v0.0.1_1
- Agregado archivo de dependencias
- Mensaje `Unknown command` cambiado por `Comando desconocido`

#### v0.0.1
- Proyecto inicial
