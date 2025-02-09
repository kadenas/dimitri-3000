import socket
import time

def test_server_bind():
    try:
        # Crear socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Intentar vincular al puerto
        addr = ('0.0.0.0', 5060)  # o '127.0.0.1' para localhost
        sock.bind(addr)
        
        print(f"Servidor vinculado exitosamente a {addr}")
        print("Esperando 30 segundos...")
        
        # Mantener el socket abierto por un momento
        time.sleep(30)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
        print("Socket cerrado")

if __name__ == "__main__":
    test_server_bind()