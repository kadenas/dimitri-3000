import pysipp
from pysipp.agent import UserAgent

def test_basic_setup():
    try:
        # Usar las funciones de cliente y servidor directamente
        client = pysipp.client(
            destaddr=('127.0.0.1', 5061),
            local_host='127.0.0.1',
            local_port=5060
        )
        print("Cliente creado exitosamente")

        server = pysipp.server(
            local_host='127.0.0.1',
            local_port=5061
        )
        print("Servidor creado exitosamente")

        # Crear un escenario básico
        scenario = pysipp.scenario()
        print("Escenario creado exitosamente")

        return True
    except Exception as e:
        print(f"Error en la prueba: {str(e)}")
        return False

def test_simple_connectivity():
    """Prueba básica de conectividad usando sockets."""
    import socket
    try:
        # Prueba UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 5060))
        print("Socket UDP creado exitosamente")
        sock.close()

        # Prueba TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 5060))
        print("Socket TCP creado exitosamente")
        sock.close()

        return True
    except Exception as e:
        print(f"Error en prueba de conectividad: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Probando PySIPP ===")
    success_pysipp = test_basic_setup()
    print(f"\nResultado PySIPP: {'Éxito' if success_pysipp else 'Fallo'}")

    print("\n=== Probando Conectividad Básica ===")
    success_socket = test_simple_connectivity()
    print(f"\nResultado Conectividad: {'Éxito' if success_socket else 'Fallo'}")
