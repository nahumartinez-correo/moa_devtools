# --------------------------------------------------------------
# parser/field_109/parser_109_110011.py
# Campo 109 para código 110011
# Crear la orden de pago con QR
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

        # Layout específico para el código 110011 - Crear la orden de pago con QR
        match "110011":

            case "110011":
                mp_amount = seg(12)
                mp_description = seg(20)
                mp_device_name = seg(9)
                mp_ext_reference = seg(12)
                mp_quantity = seg(1)

                return {
                    "nombre": "Campo 109 (110011 - QR)",
                    "mp_amount": mp_amount,
                    "mp_description": mp_description,
                    "mp_device_name": mp_device_name,
                    "mp_ext_reference": mp_ext_reference,
                    "mp_quantity": mp_quantity,
                    "raw": raw_dummy + data
                }
