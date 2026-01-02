# --------------------------------------------------------------
# Simulador_MP_response_100011.py
# Respuesta para código de procesamiento 100011 (crear orden con Smart Point).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log
from Simulador_MP_order_state import (
    build_identifier,
    build_numeric_reference,
    clear_current_order,
    get_current_order,
    get_request_datetime,
    is_order_expired,
    set_current_order,
)
import random


class Response100011:
    """
    Generador de campos asociados al código de procesamiento 100011.
    Cada campo puede variar según la condición simulada.
    """

    @staticmethod
    def build_field(responder, numero_de_bit: int):
        """
        Construye un campo ISO8583 para este código.

        Parámetros
        ----------
        responder : Responder
            Instancia del orquestador.
        numero_de_bit : int
            Campo que debe generarse.

        Retorno
        -------
        None
        """

        condicion = responder.condicion
        parsed_fields = responder.parsed.get("parsed_fields", {})

        # =======================================================
        # ============= 1) MATCH POR CONDICIÓN ===================
        # =======================================================
        match condicion:

            # --------------------------
            # Condición: SERVER_DOWN
            # --------------------------
            case "server_down":
                match numero_de_bit:

                    case 105:
                        http_code = "500".ljust(4)
                        error_code = "9999".ljust(4)
                        message = "SERVER DOWN".ljust(492)

                        contenido = (http_code + error_code + message).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Datos de orden de pago (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        # --- LOGUEO ---
                        log(f"[ 100011 - Smart Point / server_down ] Campo 105 generado:")
                        log(f"  http_code  = {http_code.strip()}")
                        log(f"  error_code = {error_code.strip()}")
                        log(f"  message    = {message.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return


            # =======================================================
            # ============= 2) DEFAULT (RESPUESTA NORMAL) ============
            # =======================================================
            case _:
                match numero_de_bit:

                    # --------------------------
                    # Campo 105 normal
                    # --------------------------
                    case 105:
                        request_dt = get_request_datetime(parsed_fields)
                        current_order = get_current_order()

                        if is_order_expired(current_order, request_dt):
                            log("[ 100011 ] Orden expirada por timeout. Se limpia el estado global.")
                            clear_current_order()
                            current_order = None

                        if current_order:
                            response_code = "409".ljust(200)
                            response_error = "409 - Conflict".ljust(100)
                            response_msg = "There is already a queued order on the terminal.".ljust(100)
                            response_cause = "already_queued_orderon_terminal".ljust(100)

                            contenido_conflicto = (
                                response_code +
                                response_error +
                                response_msg +
                                response_cause
                            ).encode("ascii")

                            longitud_conflicto = len(contenido_conflicto)
                            raw_conflicto = responder.int_to_bcd_2bytes(longitud_conflicto) + contenido_conflicto

                            responder.fields_copy[105] = {
                                "nombre": "Datos de orden de pago (conflicto)",
                                "valor": "Campo 105 generado (conflicto 409)",
                                "raw": raw_conflicto
                            }

                            log("[ 100011 ] Conflicto: ya existe una orden activa. Se devuelve 409.")
                            return

                        order_id = build_identifier("ORD").ljust(32)
                        payment_id = build_identifier("PAY").ljust(32)
                        payment_status = "created".ljust(32)
                        payment_ref = build_numeric_reference().ljust(16)
                        mp_order_status = "created".ljust(15)
                        mp_status_detail = "created".ljust(30)
                        dummy = "".ljust(339)

                        contenido = (
                            "201".ljust(4) +
                            order_id +
                            payment_id +
                            payment_status +
                            payment_ref +
                            mp_order_status +
                            mp_status_detail +
                            dummy
                        ).encode("ascii")

                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Datos de orden de pago",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        set_current_order({
                            "order_id": order_id.strip(),
                            "payment_id": payment_id.strip(),
                            "payment_status": "created",
                            "payment_ref": payment_ref.strip(),
                            "mp_order_status": "created",
                            "mp_status_detail": "created",
                            "created_at": request_dt,
                            "pending_status_polls": random.randint(0, 2)
                        })

                        # Logueo detallado
                        log(f"[ 100011 - Smart Point / OK ] Campo 105 generado:")
                        log(f" - Http_code: 201")
                        log(f" - Order_id: {order_id.strip()}")
                        log(f" - Payment_id: {payment_id.strip()}")
                        log(f" - Payment_status: {payment_status.strip()}")
                        log(f" - Payment_ref: {payment_ref.strip()}")
                        log(f" - mp_order_status: {mp_order_status.strip()}")
                        log(f" - mp_status_detail: {mp_status_detail.strip()}")
                        log(" - Relleno: 339 bytes")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return
