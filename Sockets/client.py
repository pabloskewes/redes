import jsockets

import filecmp
import sys, threading

s = jsockets.socket_udp_connect("anakena.dcc.uchile.cl", 1818)
if s is None:
    print("could not open socket")
    sys.exit(1)

Archivo_Entrada = sys.argv[1]
Max_Paquetes = sys.argv[2]


def int_to_string_bytearray(a: int) -> bytearray:
    return f"{a}".encode("utf-8")


def string_bytearray_to_int(b: bytearray) -> int:
    return int(b.decode("utf-8"))


print('% Inicio del "handshake" %')


print('Cliente envía: "Hola" ')
s.send(b"Hola")

respuesta = s.recv(1500)
print("Servidor responde: " + respuesta.decode())


s.send(int_to_string_bytearray(Max_Paquetes.zfill(5)))
print("Cliente envía: " + Max_Paquetes)

respuesta2 = string_bytearray_to_int(s.recv(1500))
print("Servidor responde: " + str(respuesta2))


print('% Fin del "handshake" %')
print("% A partir de este punto, el cliente puede enviar paquetes arbitrarios. %")


# def generate_packet(byte_size):
#    s = '0'
#    i = 0
#    while len(s) < byte_size:
#        i = (i + 1) % 10
#       s += str(i)
#    with open(f"archivo_de_entrada.txt", 'w') as f:
#        f.write(s)


# generate_packet(50)


def comparacion(archivo_1, archivo_2):
    if filecmp.cmp(archivo_1, archivo_2):
        print("Los archivos son iguales.")
    else:
        print("Los archivos son distintos.")


def Rdr(s):
    with open(f"archivo_de_entrada.txt", "w") as f:
        f.write("")

    while True:
        try:
            data = s.recv(respuesta2).decode()
        except:
            data = None
        if not data:
            break

        with open(f"archivo_de_entrada.txt", "w") as f:
            f.write(data)

        print("Servidor responde:   " + data, end="")

    comparacion(Archivo_Entrada, "archivo_de_entrada.txt")


newthread = threading.Thread(target=Rdr, args=(s,))
newthread.start()

with open(Archivo_Entrada, "r") as f:
    byte = f.read(respuesta2)
    while byte:
        s.send(byte.encode())
        print("Cliente envía: " + byte, end="")
        byte = f.read(respuesta2)

    f.close()
