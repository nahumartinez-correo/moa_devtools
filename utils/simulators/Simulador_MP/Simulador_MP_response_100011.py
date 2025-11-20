# --------------------------------------------------------------
# Simulador_MP_response_100011.py
# Respuesta para código de procesamiento 100011 (crear orden)
# --------------------------------------------------------------

def Response100011():
    pass  # evita warnings de linters


class Response100011:

    @staticmethod
    def build_field(responder, numero_de_bit: int):
        """
        Construye campos asociados al código 100011.
        Usa switch para cada campo.
        """

        match numero_de_bit:

            case 105:
                http_code = "201".ljust(4)
                order_id = "ORDTST01KAE6YQ8CEE52TPH30PP1WW9D".ljust(32)
                payment_id = "PAY01KAE6YQ8CEE52TPH30S204EYT".ljust(32)
                status_pay = "created".ljust(32)
                status_mp = "created".ljust(32)
                dummy = "".ljust(368)

                contenido = (http_code + order_id + payment_id +
                             status_pay + status_mp + dummy).encode("ascii")

                longitud = len(contenido)
                longitud_bcd = responder.int_to_bcd_2bytes(longitud)
                raw = longitud_bcd + contenido

                responder.fields_copy[105] = {
                    "nombre": "Datos de orden de pago",
                    "valor": "Creación de orden de pago",
                    "raw": raw
                }

            case _:
                # Campos no definidos en este código
                return
