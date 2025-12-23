# --------------------------------------------------------------
# parser/field_109/parser_109_200025.py
# Campo 109 para código 200025
# Reembolso de pago con Smart Point
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

        # Layout específico para el código 200025 - Reembolso de un pago
        match "200025":

            case "200025":
                mp_order_id_PS = seg(32)

                return {
                    "nombre": "Campo 109 (200025 - Smart Point)",
                    "mp_order_id_PS": mp_order_id_PS,
                    "raw": raw_dummy + data
                }