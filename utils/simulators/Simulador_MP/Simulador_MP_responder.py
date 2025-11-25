# --------------------------------------------------------------
# Simulador_MP_responder.py
# Orquestador de respuestas: aplica reglas generales, determina
# condición simulada y delega la construcción de campos a los
# módulos específicos por código de procesamiento.
# --------------------------------------------------------------

from datetime import datetime
from Simulador_MP_response_100011 import Response100011
from Simulador_MP_response_100010 import Response100010
from Simulador_MP_conditions import CONDITIONS


def log(msg: str) -> None:
    """Imprime un mensaje con timestamp."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


class Responder:
    """
    Orquestador de la generación de respuestas ISO8583.

    Parámetros
    ----------
    parsed_message : dict
        Estructura generada por el parser, con campos analizados.
    interactivo : bool
        Indica si el servidor debe esperar ENTER tras cada respuesta.
    condicion : str | None
        Nombre de una condición simulada a aplicar; si no se especifica,
        la respuesta será normal.
    """

    def __init__(self, parsed_message: dict, interactivo: bool = False, condicion: str | None = None):
        self.parsed = parsed_message
        self.interactivo = interactivo
        self.condicion = condicion

        self.fields_copy = dict(self.parsed.get("parsed_fields", {}))

        bmp_primary = self.parsed.get("bitmap_primary", b"\x00" * 8)
        bmp_secondary = self.parsed.get("bitmap_secondary", b"\x00" * 8)
        self.bitmap_int = int.from_bytes(bmp_primary + bmp_secondary, "big")

        self.tcp_prefix = self.parsed.get("tcp_prefix", b"\x00\x00")

    # ----------------------------------------------------------
    # Utilidades
    # ----------------------------------------------------------

    @staticmethod
    def int_to_bcd_2bytes(n: int) -> bytes:
        """
        Convierte un entero (0–9999) a representación BCD en 2 bytes.

        Parámetros
        ----------
        n : int
            Valor a convertir.

        Retorno
        -------
        bytes
            Representación en BCD.
        """
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
        """
        Activa un bit en el bitmap interno.

        Parámetros
        ----------
        numero_de_bit : int
            Número de bit ISO8583 (1–128).
        """
        bit_pos = 128 - numero_de_bit
        self.bitmap_int |= (1 << bit_pos)

    def setear_campo_39(self):
        """
        Define el campo 39 según exista o no una condición simulada.
        Si no hay condición, se usa '00'.
        Si existe condición, se aplica el código definido en CONDITIONS.
        """

        self.activar_bit_en_bitmap(39)

        if self.condicion in CONDITIONS:
            codigo = CONDITIONS[self.condicion]["codigo_39"]
        else:
            codigo = "00"

        self.fields_copy[39] = {
            "nombre": "Código de respuesta",
            "valor": codigo,
            "raw": codigo.encode("ascii")
        }

    # ----------------------------------------------------------
    # Delegación a módulos específicos por código de procesamiento
    # ----------------------------------------------------------

    def procesar_campo(self, codigo: str, numero_de_bit: int):
        """
        Llama al módulo específico correspondiente al código
        de procesamiento recibido.

        Parámetros
        ----------
        codigo : str
            Código de procesamiento (campo 3).
        numero_de_bit : int
            Campo a construir por el módulo.

        Retorno
        -------
        None
        """

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
        """
        Construye la respuesta final ISO8583, aplicando la
        condición simulada si corresponde.

        Retorno
        -------
        bytes
            Mensaje ISO8583 final con prefijo TCP.
        """

        self.setear_campo_39()

        codigo = self.parsed.get("parsed_fields", {}).get(3, {}).get("valor", "")
        log(f"[RESPUESTA] Código de procesamiento detectado: {codigo}")

        if self.condicion in CONDITIONS:
            cfg = CONDITIONS[self.condicion]

            if cfg["usa_105"]:
                self.activar_bit_en_bitmap(105)
                self.procesar_campo(codigo, 105)

            if cfg["usa_106"]:
                self.activar_bit_en_bitmap(106)
                self.procesar_campo(codigo, 106)

            if cfg["usa_107"]:
                self.activar_bit_en_bitmap(107)
                self.procesar_campo(codigo, 107)

        else:
            self.activar_bit_en_bitmap(105)
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
