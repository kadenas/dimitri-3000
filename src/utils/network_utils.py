import netifaces
from typing import Optional

def get_local_ip() -> Optional[str]:
    """
    Obtiene la IP local principal del sistema.
    Prioriza interfaces que no sean localhost y que estén activas.
    """
    try:
        # Obtener todas las interfaces de red
        interfaces = netifaces.interfaces()
        
        # Filtrar loopback (lo)
        interfaces = [i for i in interfaces if i != 'lo']
        
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            # Buscar direcciones IPv4
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    # Evitar IPs locales y de docker
                    if not ip.startswith('127.') and not ip.startswith('172.'):
                        return ip
        
        # Si no encontramos una IP adecuada, retornar None
        return None
    except Exception as e:
        print(f"Error obteniendo IP local: {e}")
        return None