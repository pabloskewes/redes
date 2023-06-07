from typing import List
import random
from socket import timeout as SocketTimeout


def is_in_circular_range(num: int, start: int, end: int) -> bool:
    """
    Verifica si un número está en un rango circular.

    Args:
        num: número a verificar
        start: inicio del rango
        end: fin del rango

    Returns:
        True si num está en el rango, False en otro caso
    """
    if start <= end:
        return start <= num <= end
    return start <= num or num <= end


def send_data_with_loss(
    socket, data: bytes, loss_rate: float = 0, verbose: bool = False
) -> None:
    """
    Envía un paquete con loss_rate porcentaje de pérdida

    Args:
        socket: socket UDP
        data: datos a enviar (bytes)
        loss_rate: porcentaje de pérdida (por defecto 0)
        verbose: si es True, imprime un mensaje cada vez que se pierde un paquete
    """
    if random.random() > loss_rate:
        socket.send(data)
    else:
        if verbose:
            print("[send_loss]")


def recv_data_with_loss(socket, loss_rate: float = 0, verbose: bool = False) -> bytes:
    """
    Recibe un paquete con loss_rate porcentaje de pérdida

    Args:
        socket: socket UDP
        size: tamaño del paquete a recibir
        loss_rate: porcentaje de pérdida (por defecto 0)

    Returns:
        datos recibidos (bytes)
    """
    if random.random() > loss_rate:
            data = socket.recv(1024)
            return data
    else:
        if verbose:
            print("[recv_loss]")



def send_message_with_retry(
    socket,
    message: bytes,
    max_retries: int = 5,
    timeout: int = 10,
    verbose: bool = False,
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
            if verbose:
                print(f"Timeout, reenviando mensaje ({i+1}/{max_retries})")
    if verbose:
        print("Se alcanzó el número máximo de reintentos")

    raise Exception("Se alcanzó el número máximo de reintentos")


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


def int_to_str(i: int, length: int) -> str:
    """
    Convierte un entero a un string de largo length.

    Args:
        i: entero a convertir
        length: largo del string

    Returns:
        string
    """
    if i >= 10**length:
        raise ValueError("El entero es más largo que el largo especificado")
    return str(i).zfill(length)
