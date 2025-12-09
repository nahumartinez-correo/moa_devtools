# --------------------------------------------------------------
# parser/field_109/parser_109_100011.py
# Campo 109 para código 100010
# Consultar el status de la orden de pago con Smart Point
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

        # Layout específico para el código 100010 - Consultar el status de la orden de pago
        match "100010":

            case "100010":
                mp_order_id_PS = seg(32)

                return {
                    "nombre": "Campo 109 (100010)",
                    "mp_order_id_PS": mp_order_id_PS,
                    "raw": raw_dummy + data
                }
