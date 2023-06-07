# Tarea 2 - Pablo Skewes

## Contenido del "repositorio"

- jsockets.py (libreria de sockets del curso)
- go_back_n.py (codigo implementación del protocolo Go-Back-N)
- medidor_bw_udp.py (tarea 1)
- Readme.md (este archivo)
- requirements.txt (librerias "necesarias" para ejecutar el programa)
- tarea2_pablo_skewes.ipynb (notebook con respuestas a las preguntas de la tarea)
- tarea2_pablo_skewes.pdf (preview del notebook en pdf)
- Imagenes y cliente y servidor hecho por el profesor

## Cómo "instalar" el programa

Para ejecutar el programa se recomienda instalar las librerias necesarias con el siguiente comando:

```bash
python-mvenvvenv
sourcevenv/bin/activate
pipinstall-rrequirements.txt

```


## Uso del programa

Aquí va un ejemplo de como se puede usar el programa:

```bash

python go_back_n.py
--packet-size 2000 
--window-size 10
--timeout 20
--loss 0.1
--filepath./Tarea1_Redes.pdf
--server-url anakena.dcc.uchile.cl
 --server-port 1819

```

De todas formas, todos los parametros tienen un valor por defecto, por lo que se puede ejecutar el programa sin ningun parametro y debería funcionar. (Sin linux, no se tendría el /etc/services por lo que habría que usar otro archivo).
