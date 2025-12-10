# --------------------------------------------------------------
# parser/field_109/parser_109_210010.py
# Campo 109 para código 210010
# Consulta de pago QR Integrado
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

        # Layout específico para el código 210010 - Consulta un pago QR
        match "210010":

            case "210010":
                payment_id = seg(20)

                return {
                    "nombre": "Campo 109 (210010 - QR)",
                    "payment_id": payment_id,
                    "raw": raw_dummy + data
                }