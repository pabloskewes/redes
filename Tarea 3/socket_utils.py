from socket import SocketTimeout


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
