# --------------------------------------------------------------
# response_105_210015.py
# Respuesta para código de procesamiento 210015 (buscar un pago con QR).
# Construye campos 105/106/107 si corresponde, según la condición.
# --------------------------------------------------------------

from Simulador_MP_logger import log

class Response210015:
    """
    Generador de campos asociados al código de procesamiento 210015.
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
                        # [0 - 4]
                        http_code = "200".ljust(4)
                        # [5 - 9]
                        dummy_1 = "".ljust(6)
                        # [10 - 29]
                        mp_status_pago = "approved".ljust(20)
                        # [30 - 39]
                        mp_order_id = "1234567890".ljust(10)
                        # [40 - 75]
                        mp_payment_date = "26112025133000".ljust(35)
                        # [76 - 99]
                        dummy_2 = "".ljust(25)

                        # [100 - 119]
                        mp_payment_id = "1235".ljust(20)
                        # [120 - 139]
                        mp_auth_code = "12345678901234567890".ljust(20)
                        # [140 - 149]
                        mp_refund_id = "".ljust(10)
                        # [150 - 184]
                        mp_refund_date = "".ljust(35)
                        # [185 - 199]
                        dummy_3 = "".ljust(15)

                        # [200 - 219]
                        mp_description = "Pago aprobado".ljust(20)
                        # [220 - 234]
                        mp_ext_reference = "2255887744".ljust(15)
                        # [235 - 246]
                        mp_refund_amount = "".ljust(12)
                        # [245 - 299]
                        dummy_4 = "".ljust(53)

                        # [300 - 311]
                        mp_amount = "000000230000".ljust(12)
                        # [312 - 331]
                        mp_refund_status = "".ljust(20)
                        # [332 - 399]
                        dummy_5 = "".ljust(68)

                        # [400 - 439]
                        mp_payment_method = "QRI".ljust(40)
                        # [440 - 459]
                        mp_payment_type = "QRI".ljust(20)
                        # [460 - 479]
                        mp_refund_payment_id = "".ljust(20)
                        # [480 - 484]
                        mp_paging_total = "1".ljust(5)
                        # [485 - 499]
                        dummy_6 = "".ljust(15)

                        contenido = (
                            http_code +
                            dummy_1 +
                            mp_status_pago +
                            mp_order_id +
                            mp_payment_date +
                            dummy_2 +
                            mp_payment_id +
                            mp_auth_code +
                            mp_refund_id +
                            mp_refund_date +
                            dummy_3 +
                            mp_description +
                            mp_ext_reference +
                            mp_refund_amount +
                            dummy_4 +
                            mp_amount +
                            mp_refund_status +
                            dummy_5 +
                            mp_payment_method +
                            mp_payment_type +
                            mp_refund_payment_id +
                            mp_paging_total +
                            dummy_6
                        ).encode("ascii")

                        longitud = len(contenido)
                        raw = responder.int_to_bcd_2bytes(longitud) + contenido

                        responder.fields_copy[105] = {
                            "nombre": "Datos de orden de pago",
                            "valor": "Campo 105 generado (normal)",
                            "raw": raw
                        }

                        # Logueo detallado
                        log(f"[ 210015 - QR / OK ] Campo 105 generado:")
                        log(f" - Http_code: {http_code.strip()}")
                        log(f" - mp_status_pago: {mp_status_pago.strip()}")
                        log(f" - mp_order_id: {mp_order_id.strip()}")
                        log(f" - mp_payment_date: {mp_payment_date.strip()}")
                        log(f" - mp_payment_id: {mp_payment_id.strip()}")
                        log(f" - mp_auth_code: {mp_auth_code.strip()}")
                        log(f" - mp_refund_id: {mp_refund_id.strip()}")
                        log(f" - mp_refund_date: {mp_refund_date.strip()}")
                        log(f" - mp_description: {mp_description.strip()}")
                        log(f" - mp_ext_reference: {mp_ext_reference.strip()}")
                        log(f" - mp_refund_amount: {mp_refund_amount.strip()}")
                        log(f" - mp_amount: {mp_amount.strip()}")
                        log(f" - mp_refund_status: {mp_refund_status.strip()}")
                        log(f" - mp_payment_method: {mp_payment_method.strip()}")
                        log(f" - mp_payment_type: {mp_payment_type.strip()}")
                        log(f" - mp_refund_payment_id: {mp_refund_payment_id.strip()}")
                        log(f" - mp_paging_total: {mp_paging_total.strip()}")

                    case 106:
                        return

                    case 107:
                        return

                    case _:
                        return
