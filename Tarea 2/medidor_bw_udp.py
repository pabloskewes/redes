from typing import List
import argparse
import sys
import time
from socket import timeout as SocketTimeout

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, *args, **kwargs: x

import jsockets


def generate_chunks(filepath: str, chunk_size: int) -> List[bytes]:
    """Genera una lista de chunks de tamaño chunk_size a partir de un archivo."""
    chunks = []
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                chunks.append(chunk)
            else:
                break
    return chunks


def send_message_with_retry(
    socket, message: bytes, max_retries: int = 5, timeout: int = 10
) -> bytes:
    """
    Envía un mensaje y espera por una respuesta. Si no hay respuesta, reenvía el mensaje.

    Args:
        socket: socket UDP
        message: mensaje a enviar (bytes)
        max_retries: número máximo de reintentos (por defecto 5)
        timeout: tiempo de espera por respuesta (por defecto 10)

    Returns:
        respuesta del servidor (bytes)
    """

    for i in range(max_retries):
        socket.send(message)
        socket.settimeout(timeout)
        try:
            answer = socket.recv(1024)
            return answer
        except SocketTimeout:
            print(f"Timeout, reenviando mensaje ({i+1}/{max_retries})")
    print("Se alcanzó el número máximo de reintentos")

    raise Exception("Se alcanzó el número máximo de reintentos")


def compute_bandwidth(
    socket,
    packet_size: str,
    filepath: str,
    verbose: float = False,
) -> None:
    """Función principal que envía un archivo a un servidor usando UDP para medir el ancho de banda."""

    if verbose:
        print(f"Propuse paquete de tamaño: {packet_size}")

    if len(packet_size) != 4:
        raise ValueError(
            "El tamaño del paquete debe ser de 4 dígitos (para escoger 1 se debe usar 0001)"
        )

    first_message = f"C{packet_size}".encode()
    first_answer = send_message_with_retry(socket, first_message).decode()

    if verbose:
        print(f"Servidor responde: {first_answer}")

    if first_answer[0] != "C":
        print("La respuesta del servidor no es la esperada: no comienza con C")
        sys.exit(1)

    chunk_size = int(first_answer[1:])
    if verbose:
        print(f"Usando un tamaño de chunk de {chunk_size} bytes")
    data_to_send = generate_chunks(filepath=filepath, chunk_size=chunk_size)

    packets_to_send = [b"D" + chunk for chunk in data_to_send]
    if verbose:
        packets_to_send = tqdm(
            packets_to_send, desc="Enviando paquetes", unit=" paquetes"
        )

    init_time = time.time()
    for packet in packets_to_send:
        socket.send(packet)

    second_answer = send_message_with_retry(socket, message=b"E").decode()
    send_time = time.time() - init_time

    if second_answer[0] != "E":
        print("La respuesta del servidor no es la esperada: no comienza con E")
        sys.exit(1)

    bytes_received = int(second_answer[1:])
    data_size = sum([len(x) for x in data_to_send])
    size_in_mb = data_size / (1024 * 1024)

    return {
        "data_size": data_size,
        "bytes_received": bytes_received,
        "send_time": send_time,
        "bandwidth": size_in_mb / send_time,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Medidor de ancho de banda usando UDP")
    parser.add_argument(
        "--packet-size",
        type=str,
        default="1000",
        help="Tamaño de los paquetes a enviar (en bytes)",
    )
    parser.add_argument(
        "--filepath",
        type=str,
        default="/etc/services",
        help="Ruta al archivo a enviar",
    )
    parser.add_argument(
        "--server-url",
        type=str,
        default="anakena.dcc.uchile.cl",
        help="URL del servidor",
    )
    parser.add_argument(
        "--server-port",
        type=str,
        default="1818",
        help="Puerto del servidor",
    )

    args = parser.parse_args()

    # Se instancia un socket UDP
    socket = jsockets.socket_udp_connect(args.server_url, args.server_port)
    if socket is None:
        print("No se pudo abrir el socket")
        sys.exit(1)

    # Se calcula el ancho de banda con la función compute_bandwidth
    data = compute_bandwidth(
        socket=socket,
        packet_size=args.packet_size,
        filepath=args.filepath,
        verbose=True,
    )

    print(f"Se enviaron {data['data_size']} bytes")
    print(f"Se recibieron {data['bytes_received']} bytes")
    print(f"Tiempo de envío: {data['send_time']} segundos")
    print(f"Ancho de banda: {data['bandwidth']} MB/s")
