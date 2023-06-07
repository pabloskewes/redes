# Tarea 1 - Pablo Skewes

## Contenido del "repositorio"


- jsockets.py (libreria de sockets del curso)
- medidor_bw_udp.py (programa principal)
- Readme.md (este archivo)
- requirements.txt (librerias "necesarias" para ejecutar el programa)
- tarea1_pablo_skewes.ipynb (notebook con respuestas a las preguntas de la tarea)
- tarea1_pablo_skewes.pdf (preview del notebook en pdf)
- Tarea1_Redes.pdf (enunciado de la tarea que puede servir para ser usado como archivo de prueba)



## Cómo "instalar" el programa

Para ejecutar el programa se recomienda instalar las librerias necesarias con el siguiente comando:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Para el programa principal (*medidor_bw_udp.py*) es necesario tener las librerias instaladas para poder usar tqdm, en caso de no querer esto, se puede simplemente borrar el "from tqdm import tqdm", y cambiar el parámetro "verbose" de la función "compute_bandwith" a False (linea 144). Igual de todas formas hice que si no se tiene tqdm, lo reemplazo por una función que no hace nada, por lo que no debería haber problemas.

También, las librerías sirven para poder ejecutar el notebook de respuestas de la tarea (tarea1_pablo_skewes.ipynb). Además, el venv también incluye jupyterlab por lo que si se instala el venv entonces es fácil de testear desde el VSCode :)

## Uso del programa

Aquí va un ejemplo de como se puede usar el programa:

```bash
python medidor_bw_udp.py --packet-size 2000 --filepath ./Tarea1_Redes.pdf --server-url anakena.dcc.uchile.cl --server-port 1818
```
De todas formas, todos los parametros tienen un valor por defecto, por lo que se puede ejecutar el programa sin ningun parametro y debería funcionar. (Sin linux, no se tendría el /etc/services por lo que habría que usar otro archivo).