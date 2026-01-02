# --------------------------------------------------------------
# Simulador_MP_response_100010.py
# Respuesta para código de procesamiento 100010 (consultar orden).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log
from Simulador_MP_order_state import (
    clear_current_order,
    get_current_order,
    get_request_datetime,
    is_order_expired,
)


class Response100010:
    """
    Generador de campos asociados al código de procesamiento 100010.
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
                            "nombre": "Datos de consulta de status de orden de pago (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        # --- LOGUEO DETALLADO ---
                        log(f"[ 100010 / server_down ] Campo 105 generado:")
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
                            log("[ 100010 ] Orden expirada por timeout. Se limpia el estado global.")
                            clear_current_order()
                            current_order = None

                        order_id_solicitado = parsed_fields.get(109, {}).get("mp_order_id_PS", "").strip()

                        if not current_order or current_order.get("order_id") != order_id_solicitado:
                            log("No hay orden activa para el order_id consultado.")
                            responder.skip_response = True  # No se construye respuesta si no hay orden válida.
                            return

                        response_code = "200".ljust(4)
                        order_id = current_order.get("order_id", "").ljust(32)
                        payment_id = current_order.get("payment_id", "").ljust(32)
                        payment_ref = current_order.get("payment_ref", "").ljust(16)

                        pending_polls = current_order.get("pending_status_polls", 0)

                        if pending_polls > 0:
                            payment_status = "at_terminal".ljust(32)
                            mp_order_status = "at_terminal".ljust(15)
                            mp_status_detail = "at_terminal".ljust(30)
                            current_order["pending_status_polls"] = pending_polls - 1
                            clear_on_finish = False
                        else:
                            payment_status = "processed".ljust(32)
                            mp_order_status = "processed".ljust(15)
                            mp_status_detail = "processed".ljust(30)
                            clear_on_finish = True

                        dummy = "".ljust(339)

                        contenido = (
                            response_code +
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
                            "nombre": "Datos de consulta de status de orden de pago",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        if clear_on_finish:
                            clear_current_order()

                        # --- LOGUEO DETALLADO ---
                        log(f"[ 100010 / OK ] Campo 105 generado:")
                        log(f" - Http_code: {response_code.strip()}")
                        log(f" - Order_id: {order_id.strip()}")
                        log(f" - Payment_id: {payment_id.strip()}")
                        log(f" - Payment_status: {payment_status.strip()}")
                        log(f" - Payment_ref: {payment_ref.strip()}")
                        log(f" - mp_order_status: {mp_order_status.strip()}")
                        log(f" - mp_status_detail: {mp_status_detail.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return
