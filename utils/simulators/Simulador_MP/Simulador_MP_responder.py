# --------------------------------------------------------------
# Simulador_MP_responder.py
# Orquestador de respuestas: delega la construcción a submódulos.
# --------------------------------------------------------------

from datetime import datetime
from Simulador_MP_response_100011 import Response100011
from Simulador_MP_response_100010 import Response100010

def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


class Responder:

    def __init__(self, parsed_message: dict):
        self.parsed = parsed_message
        self.fields_copy = dict(self.parsed.get("parsed_fields", {}))

        bmp_primary = self.parsed.get("bitmap_primary", b"\x00" * 8)
        bmp_secondary = self.parsed.get("bitmap_secondary", b"\x00" * 8)
        self.bitmap_int = int.from_bytes(bmp_primary + bmp_secondary, "big")

        self.tcp_prefix = self.parsed.get("tcp_prefix", b"\x00\x00")

    @staticmethod
    def int_to_bcd_2bytes(n: int) -> bytes:
        """Convierte un entero 0–9999 a BCD de 2 bytes."""
        if not (0 <= n <= 9999):
            raise ValueError("Longitud fuera de rango (0–9999).")

        s = f"{n:04d}"
        high = int(s[:2])
        low = int(s[2:])

        return bytes([
            ((high // 10) << 4) | (high % 10),
            ((low  // 10) << 4) | (low  % 10)
        ])

    def activar_bit_en_bitmap(self, numero_de_bit: int):
        bit_pos = 128 - numero_de_bit
        self.bitmap_int |= (1 << bit_pos)

    def aprobar_respuesta(self):
        """Campo 39 = '00'"""
        self.fields_copy[39] = {
            "nombre": "Código de respuesta",
            "valor": "00",
            "raw": b"00"
        }

    # ----------------------------------------------------------
    # NUEVO: delegación a módulos por código de procesamiento
    # ----------------------------------------------------------
    def procesar_campo(self, codigo: str, numero_de_bit: int):
        """Llama al módulo apropiado según el código."""

        match codigo:
            case "100011":
                return Response100011.build_field(self, numero_de_bit)

            case "100010":
                return Response100010.build_field(self, numero_de_bit)

            case _:
                log(f"No hay módulo definido para el código {codigo}")

    # ----------------------------------------------------------
    # Construcción final de la respuesta ISO8583
    # ----------------------------------------------------------
    def build_response_message(self) -> bytes:

        self.activar_bit_en_bitmap(39)
        self.aprobar_respuesta()

        self.activar_bit_en_bitmap(105)

        codigo = self.parsed.get("parsed_fields", {}).get(3, {}).get("valor", "")
        log(f"[RESPUESTA] Código de procesamiento detectado: {codigo}")

        # Delegación de campos dinámicos
        self.procesar_campo(codigo, 105)

        new_bitmap = self.bitmap_int.to_bytes(16, "big")
        new_mti = b"\x02\x10"

        body = b""
        for fld in sorted(self.fields_copy.keys()):
            raw = self.fields_copy[fld].get("raw", b"")
            if isinstance(raw, str):
                raw = raw.encode()
            body += raw

        iso_msg = new_mti + new_bitmap[:8] + new_bitmap[8:] + body
        payload_len = len(iso_msg)

        final_msg = self.tcp_prefix + payload_len.to_bytes(2, "big") + iso_msg
        return final_msg
