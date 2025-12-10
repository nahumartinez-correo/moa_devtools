# --------------------------------------------------------------
# parser/field_109/parser_109_200015.py
# Campo 109 para código 200015
# Consulta de pago Point (extra info)
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

        # Layout específico para el código 200015 - Consulta de pago con datos extra Point
        match "200015":

            case "200015":
                payment_id = seg(20)

                return {
                    "nombre": "Campo 109 (200015 - Point)",
                    "payment_id": payment_id,
                    "raw": raw_dummy + data
                }