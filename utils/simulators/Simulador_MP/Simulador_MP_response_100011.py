# --------------------------------------------------------------
# Simulador_MP_response_100011.py
# Respuesta para código de procesamiento 100011 (crear orden con Smart Point).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log

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
                        http_code = "201".ljust(4)
                        order_id = "ORDTST01KAE6YQ8CEE52TPH30PP1WW9D".ljust(32)
                        payment_id = "PAY01KAE6YQ8CEE52TPH30S204EYT".ljust(32)
                        status_pago = "created".ljust(32)
                        payment_ref = "".ljust(20)
                        mp_status = "created".ljust(15)
                        dummy = "".ljust(365)

                        contenido = (
                            http_code +
                            order_id +
                            payment_id +
                            status_pago +
                            payment_ref +
                            mp_status +
                            dummy
                        ).encode("ascii")

                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Datos de orden de pago",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        # Logueo detallado
                        log(f"[ 100011 - Smart Point / OK ] Campo 105 generado:")
                        log(f" - Http_code: {http_code.strip()}")
                        log(f" - Order_id: {order_id.strip()}")
                        log(f" - Payment_id: {payment_id.strip()}")
                        log(f" - Status_pago: {status_pago.strip()}")
                        log(f" - Payment_ref: {payment_ref.strip()}")
                        log(f" - mp_status: {mp_status.strip()}")
                        log(" - Relleno: 368 bytes")


                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return
