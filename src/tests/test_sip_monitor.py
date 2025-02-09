import pytest
from src.core.sip_monitor import SIPMonitor
import time

def test_sip_monitor_initialization():
    """Test de inicialización básica del monitor."""
    monitor = SIPMonitor()
    assert not monitor.is_monitoring
    assert monitor.last_options_response is None

def test_connectivity_check():
    """Test de la función de prueba de conectividad."""
    monitor = SIPMonitor()
    
    # Prueba con localhost (debería funcionar)
    assert monitor.test_connectivity("127.0.0.1", 5060, "UDP")
    
    # Prueba con una IP inválida (no debería funcionar)
    assert not monitor.test_connectivity("256.256.256.256", 5060, "UDP")

def test_options_monitoring():
    """Test del monitoreo OPTIONS."""
    monitor = SIPMonitor()
    
    config = {
        'local_ip': '127.0.0.1',
        'local_port': 5060,
        'remote_ip': '127.0.0.1',
        'remote_port': 5061,
        'transport': 'UDP',
        'interval': 1,
        'timeout': 2
    }
    
    # Iniciar monitoreo
    assert monitor.start_options_monitoring(config)
    assert monitor.is_monitoring
    
    # Esperar un poco para que se procese al menos un OPTIONS
    time.sleep(2)
    
    # Detener monitoreo
    monitor.stop_options_monitoring()
    assert not monitor.is_monitoring

def test_double_start_monitoring():
    """Test que verifica que no se puede iniciar el monitoreo dos veces."""
    monitor = SIPMonitor()
    
    config = {
        'local_ip': '127.0.0.1',
        'local_port': 5060,
        'remote_ip': '127.0.0.1',
        'remote_port': 5061,
        'transport': 'UDP',
        'interval': 1,
        'timeout': 2
    }
    
    # Primer inicio
    assert monitor.start_options_monitoring(config)
    # Segundo inicio (debería fallar)
    assert not monitor.start_options_monitoring(config)
    
    # Limpieza
    monitor.stop_options_monitoring()

if __name__ == "__main__":
    pytest.main([__file__])
