"""
Módulo de estado compartido para la simulación de Smart Point.

Se almacena en memoria una única orden activa con los campos mínimos
necesarios para que los responders 100011 (creación) y 100010
(consulta) puedan coordinarse.
"""

from datetime import datetime, timedelta
import string
import random

# Estructura interna de la orden activa.
# Ejemplo:
# {
#     "order_id": "ORD123...",
#     "payment_id": "PAY123...",
#     "status": "created",
#     "created_at": datetime(...)
# }
_current_order: dict | None = None


def get_current_order() -> dict | None:
    """Devuelve la orden activa en memoria (o None si no existe)."""
    return _current_order


def set_current_order(order_data: dict) -> None:
    """Sobrescribe la orden activa."""
    global _current_order
    _current_order = order_data


def clear_current_order() -> None:
    """Limpia cualquier orden activa."""
    global _current_order
    _current_order = None


def get_request_datetime(parsed_fields: dict) -> datetime:
    """
    Obtiene un timestamp a partir de los campos de fecha/hora del mensaje.

    Preferencia:
    - Campo 7 (MMDDhhmmss) si está presente.
    - Campos 13 (MMDD) + 12 (hhmmss) si están presentes.
    - Datetime.now() como fallback.

    Se asume el año actual porque el layout no transporta el año.
    """
    now = datetime.now()

    try:
        if 7 in parsed_fields:
            valor = parsed_fields[7].get("valor", "")
            if len(valor) >= 10:
                month = int(valor[0:2])
                day = int(valor[2:4])
                hour = int(valor[4:6])
                minute = int(valor[6:8])
                second = int(valor[8:10])
                return now.replace(month=month, day=day, hour=hour, minute=minute, second=second, microsecond=0)

        if 13 in parsed_fields and 12 in parsed_fields:
            fecha = parsed_fields[13].get("valor", "")
            hora = parsed_fields[12].get("valor", "")
            if len(fecha) >= 4 and len(hora) >= 6:
                month = int(fecha[0:2])
                day = int(fecha[2:4])
                hour = int(hora[0:2])
                minute = int(hora[2:4])
                second = int(hora[4:6])
                return now.replace(month=month, day=day, hour=hour, minute=minute, second=second, microsecond=0)

    except Exception:
        # Si el parseo falla, se continúa con el valor por defecto.
        pass

    return now.replace(microsecond=0)


def is_order_expired(order: dict | None, reference_dt: datetime, timeout_seconds: int = 60) -> bool:
    """
    Evalúa si una orden expiró considerando el timestamp de referencia.
    """
    if not order:
        return False

    created_at = order.get("created_at")
    if not isinstance(created_at, datetime):
        return False

    return (reference_dt - created_at) > timedelta(seconds=timeout_seconds)


def build_identifier(prefix: str, length: int = 29) -> str:
    """
    Construye un identificador con prefijo fijo y sufijo aleatorio alfanumérico.
    """
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}{suffix}"


def build_numeric_reference(digits: int = 10) -> str:
    """Genera una cadena numérica aleatoria de la longitud indicada."""
    return "".join(random.choices(string.digits, k=digits))
