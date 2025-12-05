# --------------------------------------------------------------
# parser/field_109/parser_109_210015.py
# Campo 109 para código 210015
# Buscar un pago con QR
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

        # Layout específico para el código 210015 - Buscar un pago con QR
        match "210015":

            case "210015":
                mp_ext_reference = seg(15)
                mp_description = seg(20)

                return {
                    "nombre": "Campo 109 (210015 - QR)",
                    "mp_ext_reference": mp_ext_reference,
                    "mp_description": mp_description,
                    "raw": raw_dummy + data
                }
