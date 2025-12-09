# --------------------------------------------------------------
# Simulador_MP_parser.py
# Parser ISO-like para el simulador.
# El parser devuelve un diccionario con los fragmentos necesarios
# para que el generador de respuestas reconstruya la respuesta.
# --------------------------------------------------------------

import datetime

def log(msg: str) -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

def parse_iso_fields(data: bytes, active_fields: list):
    """
    Interpreta los campos ISO según su tipo, formato y longitud binaria/BCD/ASCII.
    Retorna un diccionario: campo -> { 'nombre', 'valor', 'raw', ... }.
    """
    i = 0
    parsed = {}

    def read_bytes(n):
        nonlocal i
        chunk = data[i:i+n]
        i += n
        return chunk

    # === CAMPO 2 ===
    if 2 in active_fields:
        raw = read_bytes(7)
        field_data = raw[2:]
        parsed[2] = {
            "nombre": "Bin de servicio",
            "valor": field_data.hex().upper(),
            "raw": raw
        }

    # === CAMPO 3 ===
    if 3 in active_fields:
        raw = read_bytes(3)
        valor = "".join(f"{(b >> 4) & 0xF}{b & 0x0F}" for b in raw)
        parsed[3] = {
            "nombre": "Código de procesamiento",
            "valor": valor,
            "raw": raw
        }

    # === CAMPO 7 ===
    if 7 in active_fields:
        raw = read_bytes(5)
        valor = "".join(f"{(b >> 4) & 0xF}{b & 0x0F}" for b in raw)
        parsed[7] = {
            "nombre": "Fecha y hora del mensaje",
            "valor": valor,
            "raw": raw
        }

    # === CAMPO 11 ===
    if 11 in active_fields:
        raw = read_bytes(3)
        valor = "".join(f"{(b >> 4) & 0xF}{b & 0x0F}" for b in raw)
        parsed[11] = {
            "nombre": "Número de secuencia",
            "valor": valor,
            "raw": raw
        }

    # === CAMPO 12 ===
    if 12 in active_fields:
        raw = read_bytes(3)
        valor = "".join(f"{(b >> 4) & 0xF}{b & 0x0F}" for b in raw)
        parsed[12] = {
            "nombre": "Hora del mensaje",
            "valor": valor,
            "raw": raw
        }

    # === CAMPO 13 ===
    if 13 in active_fields:
        raw = read_bytes(2)
        valor = "".join(f"{(b >> 4) & 0xF}{b & 0x0F}" for b in raw)
        parsed[13] = {
            "nombre": "Fecha del mensaje",
            "valor": valor,
            "raw": raw
        }

    # === CAMPO 24 ===
    if 24 in active_fields:
        raw = read_bytes(2)
        valor = "".join(f"{(b >> 4) & 0xF}{b & 0x0F}" for b in raw)
        parsed[24] = {
            "nombre": "Código interno",
            "valor": valor,
            "raw": raw
        }

    # === CAMPO 41 ===
    if 41 in active_fields:
        raw = read_bytes(8)
        parsed[41] = {
            "nombre": "Nodo (8 bytes ASCII)",
            "valor": raw.decode("ascii", errors="ignore").strip(),
            "raw": raw
        }

    # === CAMPO 60 ===
    if 60 in active_fields:
        raw_version = read_bytes(1)
        raw_len = read_bytes(1)
        length60 = raw_len[0]
        raw_a = read_bytes(20)
        raw_b = read_bytes(4)
        raw = raw_version + raw_len + raw_a + raw_b
        parsed[60] = {
            "nombre": "Versión de correo / Nodo / Versión código",
            "version_ascii": raw_version.hex().upper(),
            "longitud_total": length60,
            "nodo_completo": raw_a.decode("ascii", errors="ignore").strip(),
            "version_codigo": raw_b.decode("ascii", errors="ignore").strip(),
            "raw": raw
        }

    # === CAMPO 108 ===
    if 108 in active_fields:
        raw_dummy = read_bytes(2)
        longitud_bin = 21
        raw_data_108 = read_bytes(longitud_bin)
        raw = raw_dummy + raw_data_108
        try:
            sucursal = raw_data_108[0:5].decode("ascii", errors="ignore")
            cod_interno = raw_data_108[5:7].decode("ascii", errors="ignore")
            usuario = raw_data_108[7:].decode("ascii", errors="ignore")
        except Exception:
            sucursal = cod_interno = usuario = "?"
        parsed[108] = {
            "nombre": "Sucursal activa / Código interno / Usuario",
            "longitud_total": longitud_bin,
            "sucursal": sucursal.strip(),
            "codigo_interno": cod_interno.strip(),
            "usuario": usuario.strip(),
            "raw": raw
        }

    # === CAMPO 109 ===
    if 109 in active_fields:

        codigo_proc = parsed.get(3, {}).get("valor", "")

        # === leer longitud BCD (2 bytes) ===
        raw_dummy = read_bytes(2)
        byte1, byte2 = raw_dummy

        # convertir BCD a entero
        longitud_bin = (
            (byte1 >> 4) * 1000 +
            (byte1 & 0x0F) * 100 +
            ((byte2 >> 4) * 10 + (byte2 & 0x0F))
        )

        # leer los datos reales según longitud
        raw_data_109 = read_bytes(longitud_bin)

        # concatenar bloque completo
        raw = raw_dummy + raw_data_109

        # ------------------------------------------------------------
        # delegación dinámica a módulos externos
        # ------------------------------------------------------------
        try:
            # import dinámico del módulo handler
            module_name = f"parser.field_109.parser_109_{codigo_proc}"
            mod = __import__(module_name, fromlist=["Parser109"])
            parser_class = getattr(mod, "Parser109")

            parsed_109 = parser_class.parse(raw_dummy, raw_data_109)

            parsed[109] = parsed_109

        except ModuleNotFoundError:
            log(f"[WARN] No existe módulo parser_109 para código {codigo_proc}. Se carga estructura por defecto.")
            parsed[109] = {
                "nombre": "Datos operación MP (layout desconocido)",
                "longitud_total": longitud_bin,
                "raw": raw
            }
        except Exception as e:
            log(f"[ERROR] Fallo en parser_109 para código {codigo_proc}: {e}")
            parsed[109] = {
                "nombre": "Datos operación MP (error parseo)",
                "longitud_total": longitud_bin,
                "raw": raw
            }


    # === CAMPO 117 ===
    if 117 in active_fields:
        raw_dummy = read_bytes(2)
        longitud_bin = 32
        raw_firma = read_bytes(longitud_bin)
        raw = raw_dummy + raw_firma
        parsed[117] = {
            "nombre": "Firma digital",
            "longitud_total": longitud_bin,
            "firma": raw_firma.decode("ascii", errors="ignore").strip(),
            "raw": raw
        }

    return parsed


def parse_message(data: bytes):
    """
    Analiza el mensaje completo (encabezado TCP + estructura ISO-like).
    Devuelve un diccionario con:
    tcp_prefix, tcp_length, mti_bytes, bitmap_primary, bitmap_secondary, parsed_fields, body
    """
    log("===== INICIO DE PARSEO =====")
    log(f"Tamaño total recibido: {len(data)} bytes")

    tcp_prefix = data[0:2]
    tcp_length = int.from_bytes(data[2:4], "big")
    mti_bytes = data[4:6]
    bitmap_primary = data[6:14]             # 8 bytes
    bitmap_secondary = data[14:22]          # 8 bytes
    body = data[22:]

    log(f"Tipo de mensaje: {mti_bytes.hex().upper()}")
    log(f"Bitmap primario: {bitmap_primary.hex().upper()}")
    log(f"Bitmap secundario: {bitmap_secondary.hex().upper()}")

    bits_primary = ''.join(f"{byte:08b}" for byte in bitmap_primary)
    bits_secondary = ''.join(f"{byte:08b}" for byte in bitmap_secondary)
    active_fields = [i+1 for i, bit in enumerate(bits_primary + bits_secondary) if bit == '1']
    log(f"Campos activos detectados: {active_fields}")

    parsed_fields = parse_iso_fields(body, active_fields)

    # Registro de parsed_fields en consola
    log("----- CAMPOS DECODIFICADOS -----")
    for k, v in parsed_fields.items():
        log(f"Campo {k}: {v['nombre']}")
        for subk, subv in v.items():
            if subk == "nombre":
                continue
            log(f" - {subk.capitalize()}: {subv}")
    log("===== FIN DEL PARSEO =====\n")

    return {
        "tcp_prefix": tcp_prefix,
        "tcp_length": tcp_length,
        "mti_bytes": mti_bytes,
        "bitmap_primary": bitmap_primary,
        "bitmap_secondary": bitmap_secondary,
        "parsed_fields": parsed_fields,
        "body": body
    }
