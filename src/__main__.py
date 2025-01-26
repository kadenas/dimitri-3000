import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.config_manager import ConfigManager

# Añadir el directorio raíz al PYTHONPATH
current_dir = Path(__file__).parent.absolute()
root_dir = current_dir.parent  # Asumiendo que __main__.py está en src/
sys.path.append(str(root_dir))

def main():
    try:
        # Cargar configuración
        config_manager = ConfigManager()
        if not config_manager.load_config():
            print("Error: No se pudo cargar la configuración")
            return 1

        # Iniciar aplicación Qt
        app = QApplication(sys.argv)
        
        # Crear ventana principal
        window = MainWindow(config_manager=config_manager)
        window.show()
        
        # Cargar tema desde el módulo Python
        from src.ui.themes.cyber_theme import RetroCyberTheme
        app.setPalette(RetroCyberTheme.get_palette())
        app.setFont(RetroCyberTheme.get_font())
        app.setStyleSheet(RetroCyberTheme.get_stylesheet())
        
        return app.exec()
    
    except Exception as e:
        print(f"Error durante la inicialización: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())