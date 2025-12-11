# --------------------------------------------------------------
# Simulador_MP_response_210015.py
# Respuesta para código de procesamiento 210015 (búsqueda de pago QR).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log

class Response210015:
    """
    Generador de campos asociados al código de procesamiento 210015.
    Busca pagos QR por referencia externa y descripción.
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
                            "nombre": "Búsqueda de pago QR (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        log(f"[ 210015 - QR / server_down ] Campo 105 generado:")
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
                        respuesta = "200".ljust(10)
                        status_pago = "approved".ljust(20)
                        order_id = "ORDQR0001".ljust(10)
                        payment_date = "2023-08-01T12:00:00Z".ljust(35)

                        payment_id = "PAYQRSEARCH00000001".ljust(20)
                        auth_code = "AUTHQRSEARCH001".ljust(20)
                        refund_id = "".ljust(10)
                        refund_date = "".ljust(35)

                        description = "Busqueda QR".ljust(20)
                        ext_reference = "QRSEARCHREF01".ljust(15)
                        refund_amount = "000000000000".ljust(12)

                        amount = "000000010000".ljust(12)
                        refund_status = "none".ljust(20)

                        payment_method = "amex".ljust(40)
                        payment_type = "credit_card".ljust(20)
                        refund_payment_id = "".ljust(20)
                        paging_total = "00001".ljust(5)
                        filler4 = "".ljust(15)

                        bloque0 = (respuesta + status_pago + order_id + payment_date).ljust(100)
                        bloque1 = (payment_id + auth_code + refund_id + refund_date).ljust(100)
                        bloque2 = (description + ext_reference + refund_amount).ljust(100)
                        bloque3 = (amount + refund_status).ljust(100)
                        bloque4 = (payment_method + payment_type + refund_payment_id + paging_total + filler4).ljust(100)

                        contenido = (bloque0 + bloque1 + bloque2 + bloque3 + bloque4).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Búsqueda de pago QR",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        log(f"[ 210015 - QR / OK ] Campo 105 generado:")
                        log(f"  http_code      = {respuesta.strip()}")
                        log(f"  status_pago    = {status_pago.strip()}")
                        log(f"  order_id       = {order_id.strip()}")
                        log(f"  payment_id     = {payment_id.strip()}")
                        log(f"  paging_total   = {paging_total.strip()}")
                        log(f"  payment_method = {payment_method.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return