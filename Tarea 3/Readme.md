# Tarea 3 - Redes

## Contenido del repositorio

- jsockets.py (libreria de sockets del curso)
- pirate_upd.py (codigo implementación de pirata que inyecta un paquete al servidor)
- Readme.md (este archivo)
- requirements.txt (librerias necesarias para ejecutar el programa)
- client_echo3_udp.py (codigo cliente que envia un mensaje al servidor)
- server_echo_udp3.py (codigo servidor que recibe un mensaje del cliente y lo reenvia)
- tarea3.pdf (enunciado de la tarea)
- Makefile (archivo para ejecutar más facilmente el programa)
- .python-version (version de python utilizada)
- tarea3.md (informe de la tarea)


## Cómo instalar el programa

Para ejecutar el programa se recomienda instalar las librerias necesarias con el siguiente comando:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso del programa

Aquí va un ejemplo de como se puede usar el programa:
    
```bash
python sudo '/home/pabloskewes/Desktop/FCFM/Redes/Tarea 3/venv/bin/python' pirate_udp.py 
--client-ip 127.0.0.1
--client-port 35543 
--server-ip 127.0.0.1
--server-port 1818
```

Idealmente, se debe ejecutar el programa con sudo, llamando al ejecutable de python que se encuentra en la carpeta venv/bin/python. Esto es porque se necesita permisos de administrador para poder inyectar paquetes.

