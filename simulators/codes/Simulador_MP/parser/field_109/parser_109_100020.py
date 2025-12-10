# --------------------------------------------------------------
# parser/field_109/parser_109_100020.py
# Campo 109 para código 100020
# Eliminación de orden Smart Point
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

        # Layout específico para el código 100020 - Elimina una orden de pago Smart Point
        match "100020":

            case "100020":
                order_id = seg(10)

                return {
                    "nombre": "Campo 109 (100020 - Smart Point)",
                    "order_id": order_id,
                    "raw": raw_dummy + data
                }