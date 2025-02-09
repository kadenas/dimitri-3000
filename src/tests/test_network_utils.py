from src.utils.network_utils import get_local_ip

def test_get_local_ip():
    """Test para verificar que podemos obtener una IP local válida."""
    ip = get_local_ip()
    
    # La IP no debería ser None
    assert ip is not None
    
    # La IP no debería ser localhost
    assert not ip.startswith('127.')
    
    # Verificar formato básico de IP
    parts = ip.split('.')
    assert len(parts) == 4
    for part in parts:
        assert 0 <= int(part) <= 255