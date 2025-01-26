import os
import yaml
from typing import Dict, Optional

class ConfigManager:
    """Manage application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join("config", "default_config.yaml")
        self.config: Dict = {}
        
    def load_config(self) -> bool:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
            
    def save_config(self) -> bool:
        """Save current configuration to YAML file."""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
        
    def get_trunk_config(self) -> Dict:
        """Retorna configuración del SIP trunk."""
        return {
            'local_ip': self.config.get('local_ip', '127.0.0.1'),
            'local_port': self.config.get('local_port', 5060),
            'remote_ip': self.config.get('remote_ip', '127.0.0.1'),
            'remote_port': self.config.get('remote_port', 5060),
            'transport': self.config.get('transport', 'udp'),
            'keepalive_interval': self.config.get('keepalive_interval', 30)
        }

    def get(self, key: str, default=None):
        """Obtiene valor de configuración."""
        return self.config.get(key, default)