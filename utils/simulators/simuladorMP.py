import socket
import threading
from datetime import datetime
import argparse

# Se identifica el último mensaje parseado para su reutilización al armar la respuesta.
LAST_PARSED_MESSAGE = {
    "fields": {},              # diccionario: número de campo -> { "nombre": ..., "valor": ... }
    "bitmap_primary": b"",     # 8 bytes
    "bitmap_secondary": b"",   # 8 bytes (vacío si no existe)
    "bitmap_full": b"",        # 16 bytes (siempre el conjunto con el que vino)
    "mti_bytes": b"",          # 2 bytes MTI original
    "tcp_prefix": b"",         # 2 bytes prefijo TCP recibido (por compatibilidad)
}

# ------------------------------------------------------------------------------------------------------------------------

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# ------------------------------------------------------------------------------------------------------------------------

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Servidor ISO8583 Emulador MercadoPago"
    )
    parser.add_argument(
        "--use105",
        action="store_true",
        help="Incluir el campo 105 en las respuestas (por defecto no se incluye)."
    )

    args = parser.parse_args()

# ------------------------------------------------------------------------------------------------------------------------

# ==========================================================
# 🔍 FUNCIONES DE PARSEO
# ==========================================================

def parse_iso_fields(data: bytes, active_fields: list):
    """
    Interpreta los campos ISO según su tipo, formato y longitud binaria/BCD/ASCII.
    """
    i = 0
    parsed = {}

    # ------------------------------------------------------------------------------------------------------------------------

    def read_bytes(n):
        nonlocal i
        chunk = data[i:i+n]
        i += n
        return chunk

    # ------------------------------------------------------------------------------------------------------------------------

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
        raw_dummy = read_bytes(2)
        longitud_bin = 177
        raw_data_109 = read_bytes(longitud_bin)
        raw = raw_dummy + raw_data_109
        idx = 0

        def seg(n):
            """Extrae un segmento ASCII de longitud fija desde raw_data_109."""
            nonlocal idx
            s = raw_data_109[idx:idx+n].decode("ascii", errors="ignore")
            idx += n
            return s.strip()

        # Desglose según el nuevo layout
        tipo_terminal = seg(5)
        external_reference = seg(11)
        operador_id = seg(5)
        anio = seg(4)
        mes = seg(2)
        dia = seg(2)
        hora = seg(6)
        secuenciador = seg(8)
        monto = seg(12)
        ticket = seg(20)
        imprime_ticket = seg(2)
        medio_pago = seg(20)
        cuotas = seg(2)
        serial = seg(72)

        parsed[109] = {
            "nombre": "Datos de operación MP (nuevo layout)",
            "longitud_total": longitud_bin,
            "tipo_terminal": tipo_terminal,
            "external_reference": external_reference,
            "operador_id": operador_id,
            "anio": anio,
            "mes": mes,
            "dia": dia,
            "hora": hora,
            "secuenciador": secuenciador,
            "monto": monto,
            "ticket": ticket,
            "imprime_ticket": imprime_ticket,
            "medio_pago": medio_pago,
            "cuotas": cuotas,
            "serial_device": serial,
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

# ------------------------------------------------------------------------------------------------------------------------

def parse_message(data: bytes):
    """Analiza el mensaje completo (encabezado TCP + estructura ISO-like)."""
    log("===== INICIO DE PARSEO =====")
    log(f"Tamaño total recibido: {len(data)} bytes")

    # tcp_prefix y longitud se mantendrán para la reconstrucción
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

    # Se parsean los campos y se guarda la información en LAST_PARSED_MESSAGE
    parsed_fields = parse_iso_fields(body, active_fields)

    # Se registran los resultados en la variable global para su uso al construir la respuesta.
    LAST_PARSED_MESSAGE["fields"] = parsed_fields
    LAST_PARSED_MESSAGE["bitmap_primary"] = bitmap_primary
    LAST_PARSED_MESSAGE["bitmap_secondary"] = bitmap_secondary
    LAST_PARSED_MESSAGE["bitmap_full"] = bitmap_primary + bitmap_secondary
    LAST_PARSED_MESSAGE["mti_bytes"] = mti_bytes
    LAST_PARSED_MESSAGE["tcp_prefix"] = tcp_prefix

    # Se presentan los campos parseados en consola para verificación.
    log("----- CAMPOS DECODIFICADOS -----")
    for k, v in parsed_fields.items():
        log(f"Campo {k}: {v['nombre']}")
        for subk, subv in v.items():
            if subk == "nombre":
                continue
            log(f" - {subk.capitalize()}: {subv}")
    log("===== FIN DEL PARSEO =====\n")

# ------------------------------------------------------------------------------------------------------------------------

# Función auxiliar para activar un bit en el bitmap
def activar_bit_en_bitmap(numero_de_bit: int, bitmap_int: int) -> int:
    """
    Activa un bit en el bitmap ISO (1-128).
    Si el bit corresponde al campo 39, llama a aprobar_respuesta().
    En caso contrario, llama a agregar_campo_en_respuesta().
    """
    global FIELDS_RESPONSE_COPY

    # Calcular posición real del bit
    bit_pos = 128 - numero_de_bit
    bitmap_int |= (1 << bit_pos)

    if numero_de_bit == 39:
        aprobar_respuesta()
    else:
        agregar_campo_en_respuesta(numero_de_bit)

    return bitmap_int

# ------------------------------------------------------------------------------------------------------------------------

# Función auxiliar para agregar un campo en la respuesta
def agregar_campo_en_respuesta(numero_de_bit: int):
    """
    Agrega el contenido RAW de un campo en la respuesta según el código de procesamiento (campo 3),
    utilizando una estructura de doble switch/select.
    """
    global FIELDS_RESPONSE_COPY, FIELDS_RESPONSE_COPY
    parsed_fields = LAST_PARSED_MESSAGE.get("fields", {})
    codigo_procesamiento = parsed_fields.get(3, {}).get("valor", "")

    log(f"[RESPUESTA] Preparando campo {numero_de_bit} para código de procesamiento {codigo_procesamiento}")

    # ======================================================
    # SWITCH PRINCIPAL: Código de procesamiento
    # ======================================================
    match codigo_procesamiento:
        # --------------------------------------------------
        case "100011":
            # Crear orden de pago (Smart Point)
            log("Caso 100011 → Crear orden de pago")

            # === SWITCH SECUNDARIO: Campo ===
            match numero_de_bit:
                case 105:
                    # Campo 105: Estructura con longitud BCD + 200 + OrderID + Status
                    log("Generando campo 105 (estructura con longitud BCD)")

                    # Datos simulados para pruebas
                    http_code = "200".ljust(20)
                    status = "Created".ljust(80)
                    order_id = "ORDTST01K9G23S2HB2VGJYFE0679GTCJ".ljust(32)

                    # Armar bloque de datos ASCII
                    contenido_ascii = (http_code + status + order_id).encode("ascii")
                    longitud_total = len(contenido_ascii)

                    # Longitud en BCD (2 bytes)
                    longitud_bcd = bytes([
                        0x00,  # primer byte en cero
                        ((longitud_total // 10) << 4) | (longitud_total % 10)
                    ])

                    raw_105 = longitud_bcd + contenido_ascii

                    FIELDS_RESPONSE_COPY[105] = {
                        "nombre": "Datos de orden de pago (estructura nueva)",
                        "valor": f"HTTP {http_code.strip()} / ID {order_id.strip()} / Status {status.strip()}",
                        "raw": raw_105
                    }

                    log(f"Campo 105 generado: Longitud {longitud_total} bytes (BCD={longitud_bcd.hex().upper()})")
                    log(f" - HTTP Code: {http_code.strip()}")
                    log(f" - Order ID : {order_id.strip()}")
                    log(f" - Status    : {status.strip()}")


        # --------------------------------------------------
        case "100010":
            # Consulta orden de pago (Smart Point)
            log("Caso 100010 → Consulta orden de pago")

            # === SWITCH SECUNDARIO: Campo ===
            match numero_de_bit:
                case 105:
                    bloque0 = "200     approved ".ljust(100)
                    bloque1 = "ORDENEXISTENTE".ljust(100)
                    bloque2 = "".ljust(100)
                    bloque3 = "".ljust(100)
                    bloque4 = "".ljust(100)

                    contenido = (bloque0 + bloque1 + bloque2 + bloque3 + bloque4).encode("ascii")
                    longitud = len(contenido).to_bytes(2, "big")
                    raw_105 = longitud + contenido

                    FIELDS_RESPONSE_COPY[105] = {
                        "nombre": "Datos de orden de pago (consulta)",
                        "valor": "HTTP 200 / approved / ID ORDENEXISTENTE",
                        "raw": raw_105
                    }

                    log("Campo 105 generado (consulta orden de pago).")

                case _:
                    log(f"Campo {numero_de_bit} no definido para el código {codigo_procesamiento}")

        # --------------------------------------------------
        case _:
            # Código de procesamiento no reconocido
            log(f"Código de procesamiento {codigo_procesamiento} no tiene lógica definida.")

# ------------------------------------------------------------------------------------------------------------------------
# Función auxiliar para setear el código de aprobación (campo 39)
def aprobar_respuesta():
    """Agrega el campo 39 con código '00'."""
    global FIELDS_RESPONSE_COPY
    FIELDS_RESPONSE_COPY[39] = {
        "nombre": "Código de respuesta",
        "valor": "00",
        "raw": b"00"
    }

# ------------------------------------------------------------------------------------------------------------------------
# Nueva versión de build_response_message()
def build_response_message() -> bytes:
    """
    Construye la respuesta replicando los fragmentos RAW de cada campo recibido,
    cambiando MTI 0200->0210, y utilizando funciones auxiliares para manejar
    los bits y campos de la respuesta.
    """

    global FIELDS_RESPONSE_COPY
    parsed_fields = LAST_PARSED_MESSAGE.get("fields", {})
    bmp_primary = LAST_PARSED_MESSAGE.get("bitmap_primary", b"\x00" * 8)
    bmp_secondary = LAST_PARSED_MESSAGE.get("bitmap_secondary", b"\x00" * 8)
    tcp_prefix = LAST_PARSED_MESSAGE.get("tcp_prefix", b"\x00\x00")

    # Clonamos los campos recibidos
    FIELDS_RESPONSE_COPY = dict(parsed_fields)

    # Bitmap completo en entero para manipulación
    bitmap_int = int.from_bytes(bmp_primary + bmp_secondary, "big")

    # --- Agregamos los campos necesarios ---
    bitmap_int = activar_bit_en_bitmap(39, bitmap_int)   # Campo 39

    bitmap_int = activar_bit_en_bitmap(105, bitmap_int)  # Campo 105 (según tipo de operación)

    # Bitmap actualizado a bytes
    new_bitmap = bitmap_int.to_bytes(16, "big")
    new_bmp_primary = new_bitmap[:8]
    new_bmp_secondary = new_bitmap[8:]

    # MTI fijo: 0210
    new_mti = b"\x02\x10"

    # Concatenar los RAWs en orden numérico
    body = b""
    for fld in sorted(FIELDS_RESPONSE_COPY.keys()):
        fld_entry = FIELDS_RESPONSE_COPY[fld]
        raw = fld_entry.get("raw", b"")
        body += raw

    # Armar mensaje ISO completo
    iso_msg = new_mti + new_bmp_primary + new_bmp_secondary + body

    # Calcular longitud TCP
    payload_len = len(iso_msg)
    length_bytes = payload_len.to_bytes(2, "big")

    # Ensamblado final
    response = tcp_prefix + length_bytes + iso_msg

    return response

# ------------------------------------------------------------------------------------------------------------------------

# ==========================================================
# 🖥️ FUNCIONES DE SERVIDOR
# ==========================================================

def handle_client(conn, addr):
    log(f"Conexión establecida desde {addr[0]}:{addr[1]}")
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                log(f"Cliente {addr} desconectado.")
                break
            log(f"Mensaje recibido ({len(data)} bytes).")

            # 🧩 Parseo del mensaje recibido
            parse_message(data)

            # 🧠 Construcción de respuesta
            response = build_response_message()

            # 📤 Enviar respuesta
            conn.sendall(response)
            log(f"Respuesta enviada ({len(response)} bytes).")
            #log(f"Respuesta HEX: {response.hex().upper()}")

    except Exception as e:
        log(f"Error en conexión con {addr}: {e}")
    finally:
        conn.close()

# ------------------------------------------------------------------------------------------------------------------------

def start_server(host='0.0.0.0', port=9999):
    log("Iniciando servidor MercadoPago (modo parseo detallado)...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    log(f"Servidor escuchando en puerto {port}")
    log("Esperando conexiones... (Ctrl+C para salir)")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        log("Servidor detenido manualmente.")
    finally:
        server.close()

# ------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    parse_arguments()
    start_server()
