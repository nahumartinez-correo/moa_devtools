# --------------------------------------------------------------
# Simulador_MP_response_200015.py
# Respuesta para código de procesamiento 200015 (consulta de pago Point extra info).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log

class Response200015:
    """
    Generador de campos asociados al código de procesamiento 200015.
    Consulta un pago y retorna datos adicionales de Smart Point.
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
                            "nombre": "Consulta pago Point extra (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        log(f"[ 200015 - Point / server_down ] Campo 105 generado:")
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
                        filler0 = "".ljust(90)

                        payment_id = "PAYPOINTEXTRA0000001".ljust(20)
                        caller_id = "CALLERPOINT000000001".ljust(20)
                        filler1 = "".ljust(60)

                        poi = "POINT OF INTEREST".ljust(40)
                        poi_type = "POINT_TYPE".ljust(40)
                        filler2 = "".ljust(20)

                        operator_id = "OP12345678".ljust(10)
                        filler3 = "".ljust(90)

                        device_name = "DEVICE001".ljust(10)
                        filler4 = "".ljust(90)

                        bloque0 = (respuesta + filler0).ljust(100)
                        bloque1 = (payment_id + caller_id + filler1).ljust(100)
                        bloque2 = (poi + poi_type + filler2).ljust(100)
                        bloque3 = (operator_id + filler3).ljust(100)
                        bloque4 = (device_name + filler4).ljust(100)

                        contenido = (bloque0 + bloque1 + bloque2 + bloque3 + bloque4).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Consulta pago Point extra",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        log(f"[ 200015 - Point / OK ] Campo 105 generado:")
                        log(f"  http_code   = {respuesta.strip()}")
                        log(f"  payment_id  = {payment_id.strip()}")
                        log(f"  caller_id   = {caller_id.strip()}")
                        log(f"  poi         = {poi.strip()}")
                        log(f"  poi_type    = {poi_type.strip()}")
                        log(f"  operator_id = {operator_id.strip()}")
                        log(f"  device_name = {device_name.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return