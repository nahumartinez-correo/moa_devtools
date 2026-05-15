# --------------------------------------------------------------
# Simulador_MP_response_100020.py
# Respuesta para código de procesamiento 100020 (eliminar orden Smart Point).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log

class Response100020:
    """
    Generador de campos asociados al código de procesamiento 100020.
    Elimina una orden de pago creada con Smart Point.
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
                        http_code = "500".ljust(10)
                        error_code = "9999".ljust(10)
                        message = "SERVER DOWN".ljust(80)

                        contenido = (http_code + error_code + message).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Eliminar orden Smart Point (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        # --- LOGUEO ---
                        log(f"[ 100020 - Smart Point / server_down ] Campo 105 generado:")
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
                        mp_response_code = "409".ljust(200)
                        mp_response_message = "409 - Conflict".ljust(100)
                        mp_response_cause = "the order cannot be canceled because the current status, 'processed', doesn't allow cancelation. Thecannot_cancel_order".ljust(200)

                        contenido_str = (
                            mp_response_code +
                            mp_response_message +
                            mp_response_cause
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
                        log(f"  mp_response_code    = {mp_response_code.strip()}")
                        log(f"  mp_response_message = {mp_response_message.strip()}")
                        log(f"  mp_response_cause   = {mp_response_cause.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return