# --------------------------------------------------------------
# Simulador_MP_refund_dedup_store.py
# Almacenamiento temporal en memoria para deduplicación de
# requests de refund (código 200025) por ID de campo 109.
# --------------------------------------------------------------

_refunds_processed_ids = set()


def normalize_order_id(id_109: str) -> str:
    """Normaliza el ID recibido en campo 109."""
    return str(id_109 or "").strip()


def was_processed(id_109: str) -> bool:
    """Indica si el ID 109 ya fue procesado en esta ejecución."""
    return normalize_order_id(id_109) in _refunds_processed_ids


def mark_processed(id_109: str) -> None:
    """Registra el ID 109 como procesado en memoria."""
    normalized = normalize_order_id(id_109)
    if normalized:
        _refunds_processed_ids.add(normalized)
