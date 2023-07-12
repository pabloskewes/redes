import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pirata para inyectar paquetes UDP a un cliente"
    )

    parser.add_argument(
        "--client-ip",
        type=str,
        default="127.0.0.1",
        help="IP del cliente a hackear",
    )
    parser.add_argument(
        "--client-port",
        type=str,
        default="1818",
        help="Puerto del cliente a hackear",
    )
    parser.add_argument(
        "--server-ip",
        type=str,
        default="anakena.dcc.uchile.cl",
        help="IP del servidor",
    )
    parser.add_argument(
        "--server-port",
        type=str,
        default="1818",
        help="Puerto del servidor",
    )

    args = parser.parse_args()
