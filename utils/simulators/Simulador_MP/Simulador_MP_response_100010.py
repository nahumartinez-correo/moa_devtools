# --------------------------------------------------------------
# Simulador_MP_response_100010.py
# Respuesta para código 100010 (consulta orden)
# --------------------------------------------------------------

class Response100010:

    @staticmethod
    def build_field(responder, numero_de_bit: int):

        match numero_de_bit:

            case 105:
                http_code = "200".ljust(4)
                order_id = "ORDTST01KAE6YQ8CEE52TPH30PP1WW9D".ljust(32)
                payment_id = "PAY01KAE6YQ8CEE52TPH30S204EYT".ljust(32)
                stat_pay = "at_terminal".ljust(32)
                stat_mp = "at_terminal".ljust(15)
                stat_det = "at_terminal".ljust(30)

                contenido = (http_code + order_id + payment_id +
                             stat_pay + stat_mp + stat_det).encode("ascii")

                longitud = len(contenido)
                longitud_bcd = responder.int_to_bcd_2bytes(longitud)
                raw = longitud_bcd + contenido

                responder.fields_copy[105] = {
                    "nombre": "Consulta de orden",
                    "valor": "Consulta orden",
                    "raw": raw
                }

            case _:
                return
