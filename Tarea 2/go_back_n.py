from typing import List
import argparse
import sys
from dataclasses import dataclass

import jsockets
from socket_utils import (
    generate_chunks,
    send_message_with_retry,
    send_data_with_loss,
    recv_data_with_loss,
    int_to_str,
    is_in_circular_range,
)
from timer import Timer


MAX_SEQ = 100
MAX_TRIES = 20


@dataclass
class Packet:
    protocol_char: bytes
    seq: int
    data: bytes
    is_ack: bool = False

    def to_send_format(self) -> bytes:
        seq_bytes = int_to_str(self.seq, 2).encode()
        return self.protocol_char + seq_bytes + self.data

    def __str__(self):
        string = self.to_send_format().decode()
        if len(string) <= 100:
            return string
        return string[:100] + "..."
    
    
class GoBackNSender:
    def __init__(
        self,
        socket,
        packet_size: int,
        filepath: str,
        window_size: int,
        timeout: int,
        loss_rate: float,
        max_waiting_time: int = 10,
        verbose: bool = False,
    ):
        self.socket = socket
        self.packet_size = packet_size
        self.window_size = window_size
        self.timeout = timeout
        self.loss_rate = loss_rate
        self.max_waiting_time = max_waiting_time
        self.verbose = verbose
        if window_size > MAX_SEQ:
            raise Exception(f"El tamaño de la ventana no puede ser mayor a {MAX_SEQ=}")

        self.send_base = 0
        self.next_seq_num = 0
        self.packets: List[Packet] = []
        self.timeout_timer = Timer(timeout=timeout)
        self.send_timer = Timer(timeout=max_waiting_time)

        self.data_size: int = 0

        self._setup_data(filepath, packet_size)
        
    def _setup_data(self, filepath: str, packet_size: int) -> None:
        """Configura los datos a enviar."""
        chunks = generate_chunks(filepath, packet_size)
        self.data_size = sum(len(chunk) for chunk in chunks)
        packets = []
        for i, chunk in zip(range(1, len(chunks) + 1), chunks):
            seq = i % MAX_SEQ
            packets.append(Packet(protocol_char=b"D", seq=seq, data=chunk))
        last_packet = Packet(protocol_char=b"E", seq=i + 1 % MAX_SEQ, data=b"")
        packets.append(last_packet)

        self.packets = packets
        
    def send_packet(self, position: int) -> None:
        """Envía un paquete."""
        if position >= len(self.packets):
            if self.verbose:
                print(f"El paquete {position} no existe: llegamos al final de los datos")
            return
        packet = self.packets[position]
        send_data_with_loss(
            socket=self.socket,
            data=packet.to_send_format(),
            loss_rate=self.loss_rate,
            verbose=self.verbose,
        )
        
    def receive_response(self) -> str:
        """ Revisa si llego un ACK usando un socket no bloqueante"""
        self.socket.settimeout(0)
        try:
            response = recv_data_with_loss(
                socket=self.socket,
                loss_rate=self.loss_rate,
                verbose=self.verbose,
            )
            
        except BlockingIOError:
            return None
        
        if response is None:
            return None
        
        response = response.decode()
        return response

    def send_loop(self) -> bytes:
        """Inicia el loop de envío de paquetes usando el protocolo Go-Back-N y devuelve la última respuesta del servidor."""
        tries = 0
        self.send_timer.start()
        # self.timeout_timer.start()
        while True:
            # print(f"send_base: {self.send_base}, next_seq_num: {self.next_seq_num}")
            if tries > MAX_TRIES:
                raise Exception("Se alcanzó el número máximo de reintentos")
            
            if self.send_timer.has_expired():
                raise Exception("Se alcanzó el tiempo máximo de espera")
                
            if self.next_seq_num < self.send_base + self.window_size:
                self.send_packet(self.next_seq_num)
                if self.send_base == self.next_seq_num:
                    self.timeout_timer.start()
                self.next_seq_num += 1
                
            response = self.receive_response()
            if response is None:
                if self.timeout_timer.has_expired():
                    if self.verbose:
                        print(f"Timeout en intento #{tries}, reenviando ventana")
                    self.timeout_timer.reset()
                    # reenviamos toda la ventana
                    for i in range(self.send_base, self.next_seq_num):
                        self.send_packet(i)
                    tries += 1
                    # print(f"tries: {tries}")
                    continue
                continue    
            if self.verbose:
                print(f"Recibí respuesta: {response}")
                
            if len(response) > 3:
                if self.verbose:
                    print(f"Respuesta del servidor: {response}")
                    print("Fin de la comunicación")
                self.send_timer.stop()
                return response
            # ahora que sabemos que la respuesta es un ACK, solo tenemos que verificar que es uno que estemos esperando
            ack = int(response[1:])
            if self.verbose:
                print(f"ACK: {ack}")
            if not is_in_circular_range(ack, self.send_base, self.next_seq_num):
                if self.verbose:
                    print(f"ACK {ack} no está en el rango de la ventana, ignorando ACK")
                continue
            # actualizamos el send_base
            self.send_base = ack
            if self.send_base == self.next_seq_num:
                self.timeout_timer.stop()
            else:
                self.timeout_timer.reset()


def compute_bandwidth(
    socket,
    packet_size: str,
    timeout: int,
    loss: float,
    window_size: int,
    filepath: str,
    max_waiting_time: int = 60,
    verbose: bool = False,
) -> None:
    """Calcula el ancho de banda de una conexión UDP."""
    if verbose:
        print(f"{packet_size=}, {timeout=}, {loss=}, {window_size=}, {filepath=}")

    first_message = f"C00{packet_size}".encode()
    if verbose:
        print(f"Enviando mensaje: {first_message}")

    first_answer = send_message_with_retry(
        socket=socket,
        message=first_message,
        timeout=5,
        max_retries=2,
        verbose=verbose,
    )

    if verbose:
        print(f"Servidor responde: {first_answer}")

    if first_answer[0:3] != b"A00":
        if verbose:
            print("La respuesta del servidor no es la esperada: no comienza con A00")
        return None

    chunk_size = int(first_answer[3:])

    gbn = GoBackNSender(
        socket=socket,
        packet_size=chunk_size,
        filepath=filepath,
        window_size=window_size,
        timeout=timeout / 1000, # convert to seconds
        loss_rate=loss,
        max_waiting_time=max_waiting_time,
        verbose=verbose,
    )

    if verbose:
        print(f"numero de paquetes: {len(gbn.packets)}")
    response = gbn.send_loop()
    size_in_mb = gbn.data_size / (1024 * 1024)
    send_time = gbn.send_timer.total_time

    return {
        "data_size": gbn.data_size,
        "bytes_received": int(response[3:]),
        "send_time": send_time,
        "bandwidth": size_in_mb / send_time,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Medidor de ancho de banda usando UDP")
    parser.add_argument(
        "--packet-size",
        type=str,
        default="5000",
        help="Tamaño de los paquetes a enviar (en bytes)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Tiempo de espera para recibir un ACK en ms",
    )
    parser.add_argument(
        "--loss",
        type=float,
        default=0,
        help="Probabilidad de pérdida de paquetes",
    )
    parser.add_argument(
        "--window-size",
        type=int,
        default=5,
        help="Tamaño de la ventana",
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
        default="1819",
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
        timeout=args.timeout,
        loss=args.loss,
        window_size=args.window_size,
        filepath=args.filepath,
        verbose=False,
    )

    print(f"Se enviaron {data['data_size']} bytes")
    print(f"Se recibieron {data['bytes_received']} bytes")
    print(f"Tiempo de envío: {data['send_time']} segundos")
    print(f"Ancho de banda: {data['bandwidth']} MB/s")
