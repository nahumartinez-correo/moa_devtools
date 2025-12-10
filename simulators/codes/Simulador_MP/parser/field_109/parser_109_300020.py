# --------------------------------------------------------------
# parser/field_109/parser_109_300020.py
# Campo 109 para código 300020
# Eliminación de device Point Integrado
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

        # Layout específico para el código 300020 - Eliminación de device Point
        match "300020":

            case "300020":
                device_name = seg(9)

                return {
                    "nombre": "Campo 109 (300020 - Point)",
                    "device_name": device_name,
                    "raw": raw_dummy + data
                }