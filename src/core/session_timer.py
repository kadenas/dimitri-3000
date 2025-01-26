from typing import Optional
import threading
import time
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SessionState:
   start_time: datetime
   last_refresh: datetime
   refresher: str
   active: bool = True

class SessionTimer:
    def __init__(self, expires: int = 1800, min_se: int = 90):
        """
        Inicializa el manejador de Session Timers.
        
        Args:
            expires: Tiempo de expiración de sesión en segundos (default 1800s/30min)
            min_se: Mínimo Session-Expires aceptable en segundos (default 90s)
        """
        self.session_expires = expires
        self.min_se = min_se
        self.active_sessions = {}
        self.refresh_timer = None
        self.logger = logging.getLogger(__name__)

    def start_session(self, call_id: str, refresher: str = 'uac') -> None:
        """Inicia timer para una nueva sesión."""
        now = datetime.now()
        self.active_sessions[call_id] = SessionState(
            start_time=now,
            last_refresh=now,
            refresher=refresher
        )
        self._schedule_refresh(call_id)

    def _schedule_refresh(self, call_id: str) -> None:
        """Programa el próximo refresh de la sesión."""
        if call_id not in self.active_sessions:
            return
            
        session = self.active_sessions[call_id]
        if not session.active:
            return

        refresh_time = self.session_expires * 0.9  # 90% del tiempo de expiración
        self.refresh_timer = threading.Timer(
            refresh_time,
            self._handle_refresh_timeout,
            args=[call_id]
        )
        self.refresh_timer.daemon = True
        self.refresh_timer.start()

    def _handle_refresh_timeout(self, call_id: str) -> None:
        """Maneja timeout de refresh."""
        if call_id not in self.active_sessions:
            return
            
        session = self.active_sessions[call_id]
        if not session.active:
            return

        if session.refresher == 'uac':
            self._trigger_session_refresh(call_id)
        else:
            self._check_session_expiration(call_id)

    def _trigger_session_refresh(self, call_id: str) -> None:
        """Notifica que es necesario refrescar la sesión."""
        # Esta función será llamada por SIPCallHandler
        pass

    def _check_session_expiration(self, call_id: str) -> None:
        """Verifica si la sesión ha expirado."""
        if call_id not in self.active_sessions:
            return
            
        session = self.active_sessions[call_id]
        now = datetime.now()
        
        if (now - session.last_refresh).total_seconds() > self.session_expires:
            self.end_session(call_id)

    def refresh_session(self, call_id: str) -> None:
        """Actualiza timestamp de último refresh."""
        if call_id in self.active_sessions:
            self.active_sessions[call_id].last_refresh = datetime.now()
            self._schedule_refresh(call_id)

    def end_session(self, call_id: str) -> None:
        """Finaliza una sesión."""
        if call_id in self.active_sessions:
            self.active_sessions[call_id].active = False
            if self.refresh_timer:
                self.refresh_timer.cancel()
            del self.active_sessions[call_id]

    def get_headers(self) -> dict:
        """Retorna headers necesarios para Session Timer."""
        return {
            'Session-Expires': f'{self.session_expires};refresher=uac',
            'Min-SE': str(self.min_se),
            'Supported': 'timer'
        }

    def process_response_headers(self, headers: dict, call_id: str) -> None:
        """
        Procesa headers de respuesta para Session Timer.
        
        Args:
            headers: Diccionario con headers de respuesta
            call_id: ID de la llamada
        """
        if 'Session-Expires' in headers:
            parts = headers['Session-Expires'].split(';')
            if len(parts) > 1:
                expires = int(parts[0])
                refresher = parts[1].split('=')[1]
                
                self.session_expires = expires
                if call_id in self.active_sessions:
                    self.active_sessions[call_id].refresher = refresher
                    self._schedule_refresh(call_id)
                    
    def validate_session_expires(self, proposed_expires: int) -> int:
        """Valida y ajusta el valor de Session-Expires propuesto"""
        return max(self.min_se, min(proposed_expires, 7200))

    def handle_session_refresh_response(self, call_id: str, response_code: int) -> None:
        """Maneja respuesta a refresh de sesión"""
        if response_code == 200:
            self.refresh_session(call_id)
        elif response_code >= 400:
            self.end_session(call_id)

    def is_session_active(self, call_id: str) -> bool:
        """Verifica si una sesión está activa"""
        return call_id in self.active_sessions and self.active_sessions[call_id].active