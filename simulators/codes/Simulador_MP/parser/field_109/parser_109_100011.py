# --------------------------------------------------------------
# parser/field_109/parser_109_100011.py
# Campo 109 para código 100011
# Crear la orden de pago con Smart Point
# --------------------------------------------------------------

class Parser109:

    @staticmethod
    def parse(raw_dummy: bytes, data: bytes):
        idx = 0

        def seg(n):
            nonlocal idx
            s = data[idx:idx+n].decode("ascii", errors="ignore").strip()
            idx += n
            return s

        # Layout específico para el código 100011 - Crear la orden de pago con Smart Point
        match "100011":

            case "100011":
                tipo_terminal = seg(5)
                reference = seg(11)
                operador = seg(5)
                anio = seg(4)
                mes = seg(2)
                dia = seg(2)
                hora = seg(6)
                sec = seg(8)
                monto = seg(12)
                ticket = seg(20)
                imprime = seg(2)
                medio = seg(12)
                cuotas = seg(2)
                serial = seg(82)

                return {
                    "nombre": "Campo 109 (100011 - Smart Point)",
                    "tipo_terminal": tipo_terminal,
                    "external_reference": reference,
                    "operador_id": operador,
                    "anio": anio,
                    "mes": mes,
                    "dia": dia,
                    "hora": hora,
                    "secuenciador": sec,
                    "monto": monto,
                    "ticket": ticket,
                    "imprime_ticket": imprime,
                    "medio_pago": medio,
                    "cuotas": cuotas,
                    "serial_device": serial,
                    "raw": raw_dummy + data
                }
