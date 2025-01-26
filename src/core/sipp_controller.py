from typing import Dict, Optional
import os

# Manejo seguro de la importación de pysipp
PYSIPP_AVAILABLE = False
try:
    import pysipp
    PYSIPP_AVAILABLE = True
    print("Debug: pysipp importado correctamente")
except (ImportError, TypeError) as e:
    print(f"Warning: pysipp no disponible: {e}")

class SIPPController:
    """Main controller for SIPP operations."""
    
    def __init__(self, config: Dict):
        """
        Initialize SIPP controller.
        
        Args:
            config: Dictionary with configuration parameters
            {
                'local_ip': str,
                'local_port': int,
                'remote_ip': str,
                'remote_port': int,
                'transport': str  # 'udp' or 'tcp'
            }
        """
        self.config = config
        self._uac_scenario = None  # Para llamadas salientes
        self._uas_scenario = None  # Para llamadas entrantes
        self._templates_path = "config/sip_templates"
        self._call_scenario_path = os.path.join(self._templates_path, "call.xml")
        self._receive_scenario_path = os.path.join(self._templates_path, "receive_call.xml")
        
        # Estadísticas de llamadas
        self.active_calls = 0
        self.completed_calls = 0
        self.failed_calls = 0
        
        print("Debug: SIPPController inicializado con config:", config)
        
    def initialize(self) -> bool:
        """Initialize SIPP controller with current configuration."""
        try:
            # Configurar el host SIPP
            self.sipp_host = pysipp.Host(
                self.config['local_ip'],
                int(self.config['local_port'])
            )
            
            # Configurar el destino
            self.sipp_dest = pysipp.Host(
                self.config['remote_ip'],
                int(self.config['remote_port'])
            )
            
            # Cargar los escenarios
            self._load_scenarios()
            
            print("Debug: SIPP controller initialized")
            return True
            
        except Exception as e:
            print(f"Error initializing SIPP: {e}")
            return False

    def _load_scenarios(self):
        """Carga los escenarios UAC y UAS."""
        try:
            # Cargar escenario para llamadas salientes
            if os.path.exists(self._call_scenario_path):
                self._uac_scenario = pysipp.load(self._call_scenario_path)
                print("Debug: Escenario UAC cargado")
            else:
                print(f"Warning: No se encontró el archivo {self._call_scenario_path}")
            
            # Cargar escenario para llamadas entrantes
            if os.path.exists(self._receive_scenario_path):
                self._uas_scenario = pysipp.load(self._receive_scenario_path)
                print("Debug: Escenario UAS cargado")
            else:
                print(f"Warning: No se encontró el archivo {self._receive_scenario_path}")
                
        except Exception as e:
            print(f"Error cargando escenarios: {e}")
            
    def start_call(self, from_number: str, to_number: str) -> bool:
        """Inicia una llamada saliente."""
        try:
            if not self._uac_scenario:
                print("Error: Escenario UAC no cargado")
                return False
                
            print(f"Debug: Iniciando llamada de {from_number} a {to_number}")
            
            # Configurar el escenario
            scenario = self._uac_scenario.scenario(
                agents=[self.sipp_host],
                clients=[self.sipp_dest]
            )
            
            # Configurar variables del escenario
            scenario.vars = {
                'service': to_number,
                'from_user': from_number
            }
            
            # Ejecutar el escenario
            scenario.run()
            self.active_calls += 1
            print("Debug: Llamada iniciada correctamente")
            return True
            
        except Exception as e:
            print(f"Error iniciando llamada: {e}")
            self.failed_calls += 1
            return False
            
    def start_server(self) -> bool:
        """Inicia el servidor para recibir llamadas."""
        try:
            if not self._uas_scenario:
                print("Error: Escenario UAS no cargado")
                return False
                
            print("Debug: Iniciando servidor SIP")
            
            # Configurar el escenario de servidor
            scenario = self._uas_scenario.scenario(
                agents=[self.sipp_host]
            )
            
            # Ejecutar en modo servidor (background)
            scenario.run(block=False)
            print("Debug: Servidor SIP iniciado correctamente")
            return True
            
        except Exception as e:
            print(f"Error iniciando servidor: {e}")
            return False
            
    def create_call_scenario(self) -> bool:
        """Create a basic call scenario."""
        try:
            if not os.path.exists(self._call_scenario_path):
                print(f"Error: Scenario file not found: {self._call_scenario_path}")
                return False
                
            # Crear el escenario
            scenario = pysipp.load(self._call_scenario_path)
            
            # Configurar el escenario
            self._scenario = pysipp.scenario(
                agents=[self.sipp_host],
                clients=[self.sipp_dest]
            )
            
            return True
            
        except Exception as e:
            print(f"Error creating call scenario: {e}")
            return False
            
    def start_call(self) -> bool:
        """Start a single call."""
        try:
            if not self._scenario:
                if not self.create_call_scenario():
                    return False
                    
            # Ejecutar el escenario
            self._scenario.run()
            return True
            
        except Exception as e:
            print(f"Error starting call: {e}")
            return False
            
    def start_call_burst(self, rate: int, max_calls: int) -> bool:
        """
        Start call burst (metralleta mode).
        
        Args:
            rate: Calls per second
            max_calls: Maximum number of concurrent calls
        """
        try:
            if not self._scenario:
                if not self.create_call_scenario():
                    return False
                    
            # Configurar parámetros de metralleta
            self._scenario.agents[0].rate = rate
            self._scenario.agents[0].limit = max_calls
            
            # Ejecutar el escenario
            self._scenario.run()
            return True
            
        except Exception as e:
            print(f"Error starting call burst: {e}")
            return False