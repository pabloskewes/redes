import time
from typing import Any


class TimerAlreadyRunning(Exception):
    """Excepción para cuando se intenta iniciar un timer que ya está corriendo"""
    def __init__(self):
        super().__init__("Timer is already running")


class TimerNotRunning(Exception):
    """Excepción para cuando se intenta detener un timer que no está corriendo"""
    def __init__(self):
        super().__init__("Timer is not running")
        
    
class Timer:
    """Clase para medir el tiempo de ejecución de un proceso"""
    def __init__(self, timeout: int):
        self.timeout = timeout
        self.start_time = None
        self.total_time = None
        self.time_running = False
        
    def start(self):
        if self.time_running:
            raise TimerAlreadyRunning()
        self.start_time = time.time()
        self.time_running = True
        
    def stop(self):
        if not self.time_running:
            raise TimerNotRunning()
        self.total_time = time.time() - self.start_time
        self.time_running = False
        
    def current_time(self):
        if not self.time_running:
            raise TimerNotRunning()
        return time.time() - self.start_time
    
    def has_expired(self) -> bool:
        return self.current_time() >= self.timeout
    
    def reset(self):
        self.start_time = time.time()
        self.total_time = None