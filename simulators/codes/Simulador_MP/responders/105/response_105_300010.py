# --------------------------------------------------------------
# Simulador_MP_response_300010.py
# Respuesta para código de procesamiento 300010 (consulta de device Point).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log

class Response300010:
    """
    Generador de campos asociados al código de procesamiento 300010.
    Consulta un device de Smart Point.
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
                            "nombre": "Consulta device Point (server_down)",
                            "valor": "Campo 105 generado - server_down",
                            "raw": raw
                        }

                        log(f"[ 300010 - Point / server_down ] Campo 105 generado:")
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
                        http_code = "200".ljust(10)
                        device_status = "active".ljust(20)
                        device_name = "DEVICE001".ljust(20)
                        filler = "".ljust(50)

                        contenido = (http_code + device_status + device_name + filler).encode("ascii")
                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Consulta device Point",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        log(f"[ 300010 - Point / OK ] Campo 105 generado:")
                        log(f"  http_code     = {http_code.strip()}")
                        log(f"  device_name   = {device_name.strip()}")
                        log(f"  device_status = {device_status.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return