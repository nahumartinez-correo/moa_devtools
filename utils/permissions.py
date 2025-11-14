import ctypes

def es_administrador():
    """Verifica si el proceso actual tiene permisos de administrador en Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False
