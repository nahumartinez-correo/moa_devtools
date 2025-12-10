# --------------------------------------------------------------
# parser/field_109/parser_109_300010.py
# Campo 109 para código 300010
# Consulta de device Point Integrado
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

        # Layout específico para el código 300010 - Consulta de device Point
        match "300010":

            case "300010":
                device_name = seg(9)

                return {
                    "nombre": "Campo 109 (300010 - Point)",
                    "device_name": device_name,
                    "raw": raw_dummy + data
                }