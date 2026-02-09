# --------------------------------------------------------------
# Simulador_MP_response_200025.py
# Respuesta para código de procesamiento 200025 (reembolso de pago con Smart Point).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log
from Simulador_MP_order_state import build_identifier, build_numeric_reference

class Response200025:
    """
    Generador de campos asociados al código de procesamiento 200025.
    Reembolso de un pago realizado con Smart Point.
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
                        mp_response_code = "500".ljust(10)
                        mp_response_error = "9999".ljust(10)
                        mp_response_message = "SERVER DOWN".ljust(80)

                        contenido = (mp_response_code + mp_response_error + mp_response_message).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Reembolso de pago (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        log(f"[ 200025 - Refund / server_down ] Campo 105 generado:")
                        log(f"  mp_response_code  = {mp_response_code.strip()}")
                        log(f"  mp_response_error = {mp_response_error.strip()}")
                        log(f"  mp_response_message    = {mp_response_message.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return


            # --------------------------
            # Condición: request_Refund_ya_completado_anteriormente
            # --------------------------
            case "request_Refund_ya_completado_anteriormente":
                match numero_de_bit:

                    case 105:
                        mp_response_code = "409".ljust(10)
                        dummy = "".ljust(190)
                        mp_response_error = "order_already_refunded".ljust(100)
                        mp_response_message = "the order is already refunded.".ljust(100)

                        contenido = (mp_response_code + dummy + mp_response_error + mp_response_message).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Reembolso de pago (request_Refund_ya_completado_anteriormente)",
                            "valor": "Campo 105 generado - request_Refund_ya_completado_anteriormente",
                            "raw": raw
                        }

                        log(f"[ 200025 - Refund / request_Refund_ya_completado_anteriormente ] Campo 105 generado:")
                        log(f"  mp_response_code  = {mp_response_code.strip()}")
                        log(f"  mp_response_error = {mp_response_error.strip()}")
                        log(f"  mp_response_message    = {mp_response_message.strip()}")

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
                        parsed_fields = responder.parsed.get("parsed_fields", {})
                        campo_109 = parsed_fields.get(109, {})
                        order_id = str(campo_109.get("mp_order_id_PS", "") or "").strip()
                        if not order_id:
                            log("[ 200025 - Refund ] WARNING: mp_order_id_PS ausente en campo 109")

                        refund_id = build_identifier("REF", length=29)
                        payment_ref = build_numeric_reference(digits=16)

                        mp_response_code = "201".ljust(4)
                        order_id_field = order_id.ljust(32)
                        refund_id_field = refund_id.ljust(32)
                        refund_status = "processed".ljust(32)
                        payment_ref_field = payment_ref.ljust(16)
                        mp_order_status = "refunded".ljust(15)
                        mp_status_detail = "refunded".ljust(30)

                        contenido_str = (
                            mp_response_code +
                            order_id_field +
                            refund_id_field +
                            refund_status +
                            payment_ref_field +
                            mp_order_status +
                            mp_status_detail
                        )
                        contenido = contenido_str.encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Reembolso de pago (200025 - Smart Point)",
                            "valor": "Campo 105 generado (refund procesado)",
                            "raw": raw
                        }

                        log(f"[ 200025 - Refund / OK ] Campo 105 generado:")
                        log(f"  mp_response_code   = {mp_response_code.strip()}")
                        log(f"  order_id        = {order_id_field.strip()}")
                        log(f"  refund_id       = {refund_id_field.strip()}")
                        log(f"  refund_status   = {refund_status.strip()}")
                        log(f"  payment_ref     = {payment_ref_field.strip()}")
                        log(f"  mp_order_status = {mp_order_status.strip()}")
                        log(f"  mp_status_detail= {mp_status_detail.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return
