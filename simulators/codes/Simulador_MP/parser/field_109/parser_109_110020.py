# --------------------------------------------------------------
# parser/field_109/parser_109_110020.py
# Campo 109 para código 110020
# Eliminación de orden QR Integrado
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

        # Layout específico para el código 110020 - Elimina una orden de pago QR
        match "110020":

            case "110020":
                device_name = seg(10)

                return {
                    "nombre": "Campo 109 (110020 - QR)",
                    "device_name": device_name,
                    "raw": raw_dummy + data
                }