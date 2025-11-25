# --------------------------------------------------------------
# Simulador_MP_response_100011.py
# Respuesta para código de procesamiento 100011 (crear orden).
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

        match numero_de_bit:

            case 105:

                log("----- CAMPO 105 (Datos de orden de pago) -----")

                if condicion == "server_down":
                    http_code = "500".ljust(4)
                    error_code = "9999".ljust(4)
                    message = "SERVER DOWN".ljust(492)
                    contenido = (http_code + error_code + message).encode("ascii")

                    # Logueo detallado
                    log(f" - Http_code: {http_code.strip()}")
                    log(f" - Error_code: {error_code.strip()}")
                    log(f" - Message: SERVER DOWN")
                    log(f" - Relleno: 492 bytes")

                else:
                    http_code = "201".ljust(4)
                    order_id = "ORDTST01KAE6YQ8CEE52TPH30PP1WW9D".ljust(32)
                    payment_id = "PAY01KAE6YQ8CEE52TPH30S204EYT".ljust(32)
                    status_pay = "created".ljust(32)
                    status_mp = "created".ljust(32)
                    dummy = "".ljust(368)

                    contenido = (http_code + order_id + payment_id +
                                 status_pay + status_mp + dummy).encode("ascii")

                    # Logueo detallado
                    log(f" - Http_code: {http_code.strip()}")
                    log(f" - Order_id: {order_id.strip()}")
                    log(f" - Payment_id: {payment_id.strip()}")
                    log(f" - Status_pago: {status_pay.strip()}")
                    log(f" - Status_mp: {status_mp.strip()}")
                    log(" - Relleno: 368 bytes")

                longitud = len(contenido)
                raw = responder.int_to_bcd_2bytes(longitud) + contenido

                log(f" - Longitud total: {longitud} bytes")

                responder.fields_copy[105] = {
                    "nombre": "Datos de orden de pago",
                    "valor": "Campo 105 generado",
                    "raw": raw
                }

            case _:
                return
