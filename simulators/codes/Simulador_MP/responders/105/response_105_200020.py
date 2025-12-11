# --------------------------------------------------------------
# Simulador_MP_response_200020.py
# Respuesta para código de procesamiento 200020 (devolución de pago Point/QR).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log

class Response200020:
    """
    Generador de campos asociados al código de procesamiento 200020.
    Devolución de un pago realizado con Smart Point o QR Integrado.
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
                            "nombre": "Devolución de pago (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        log(f"[ 200020 - Refund / server_down ] Campo 105 generado:")
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
                        status_pago = "refunded".ljust(20)
                        order_id = "".ljust(10)
                        refund_date = "2023-08-02T10:00:00Z".ljust(35)

                        payment_id = "PAYREFUNDPOINT00001".ljust(20)
                        auth_code = "AUTHREFUND00000000".ljust(20)
                        refund_id = "REFUND0001".ljust(10)
                        refund_payment_date = refund_date

                        description = "Refund Point".ljust(20)
                        ext_reference = "REFPOINT001".ljust(15)
                        refund_amount = "000000010000".ljust(12)

                        amount = "000000010000".ljust(12)
                        refund_status = "approved".ljust(20)

                        payment_method = "visa".ljust(40)
                        payment_type = "credit_card".ljust(20)
                        refund_payment_id = "PAYREFUNDID0000001".ljust(20)

                        bloque0 = (respuesta + status_pago + order_id + refund_date).ljust(100)
                        bloque1 = (payment_id + auth_code + refund_id + refund_payment_date).ljust(100)
                        bloque2 = (description + ext_reference + refund_amount).ljust(100)
                        bloque3 = (amount + refund_status).ljust(100)
                        bloque4 = (payment_method + payment_type + refund_payment_id).ljust(100)

                        contenido = (bloque0 + bloque1 + bloque2 + bloque3 + bloque4).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Devolución de pago",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        log(f"[ 200020 - Refund / OK ] Campo 105 generado:")
                        log(f"  http_code      = {respuesta.strip()}")
                        log(f"  status_pago    = {status_pago.strip()}")
                        log(f"  refund_id      = {refund_id.strip()}")
                        log(f"  refund_amount  = {refund_amount.strip()}")
                        log(f"  refund_status  = {refund_status.strip()}")
                        log(f"  payment_method = {payment_method.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return