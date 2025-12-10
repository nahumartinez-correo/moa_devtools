# --------------------------------------------------------------
# parser/field_109/parser_109_200020.py
# Campo 109 para código 200020
# Devolución de pago Point/QR
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

        # Layout específico para el código 200020 - Devolución de un pago
        match "200020":

            case "200020":
                payment_id = seg(20)

                return {
                    "nombre": "Campo 109 (200020 - Point/QR)",
                    "payment_id": payment_id,
                    "raw": raw_dummy + data
                }