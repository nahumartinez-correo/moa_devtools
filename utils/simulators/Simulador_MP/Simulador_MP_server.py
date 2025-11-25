# --------------------------------------------------------------
# Simulador_MP_server.py
# Servidor TCP para Simulador_MP.
# Recibe mensajes, los parsea y delega a Responder, aplicando
# parámetros interactivo y condición simulada.
# --------------------------------------------------------------

import socket
import sys
import time
import os
import subprocess

from Simulador_MP_logger import log
from Simulador_MP_parser import parse_message
from Simulador_MP_responder import Responder

try:
    import psutil
    PSUTIL_AVAILABLE = True
except Exception:
    PSUTIL_AVAILABLE = False

HOST = "0.0.0.0"
PORT = 9999

def is_port_in_use(port: int) -> bool:
    """Verifica si el puerto local está ocupado."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def kill_process_on_port(port: int) -> bool:
    """
    Intenta terminar procesos que mantengan el puerto.
    Se usa psutil si está disponible; en caso contrario se recurre a netstat/taskkill.
    Retorna True si se terminó al menos un proceso.
    """
    killed_any = False
    if PSUTIL_AVAILABLE:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.laddr.port == port:
                pid = conn.pid
                try:
                    p = psutil.Process(pid)
                    log(f"Terminando proceso PID {pid} ({p.name()}) que usa puerto {port}")
                    p.kill()
                    killed_any = True
                except Exception as e:
                    log(f"No se pudo terminar PID {pid}: {e}")
    else:
        try:
            out = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True, text=True)
            lines = out.strip().splitlines()
            pids = set()
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    pids.add(parts[-1])
            for pid in pids:
                try:
                    subprocess.check_call(f'taskkill /F /PID {pid}', shell=True)
                    log(f"PID {pid} terminado.")
                    killed_any = True
                except Exception as e:
                    log(f"No se pudo terminar PID {pid}: {e}")
        except subprocess.CalledProcessError:
            # no se encontraron procesos
            pass
    return killed_any

def clear_screen():
    """Limpia la consola."""
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        pass

def start_server(interactivo: bool = False, condicion: str | None = None):
    """
    Inicia el servidor TCP y maneja un cliente a la vez.

    Parámetros
    ----------
    interactivo : bool
        Si es True, el servidor esperará ENTER tras cada respuesta.
    condicion : str | None
        Condición simulada a aplicar en todas las respuestas.
    """

    log(f"Iniciando Simulador_MP (escucha puerto 9999)... Interactivo={interactivo}, Condición={condicion}")

    if is_port_in_use(PORT):
        log(f"Puerto {PORT} detectado como ocupado. Se intentará liberar.")
        if kill_process_on_port(PORT):
            log("Puerto liberado. Reintentando en 1 segundo.")
            time.sleep(1)
        else:
            log("No fue posible liberar el puerto automáticamente. Abortando.")
            sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        log(f"Servidor escuchando en {HOST}:{PORT}")

        try:
            while True:
                log("Esperando conexión entrante...")
                conn, addr = server.accept()
                log(f"Conexión establecida desde {addr[0]}:{addr[1]}")

                with conn:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            log("Cliente desconectado.")
                            break

                        log(f"Mensaje recibido ({len(data)} bytes).")
                        parsed = parse_message(data)

                        responder = Responder(
                            parsed,
                            interactivo=interactivo,
                            condicion=condicion
                        )

                        response = responder.build_response_message()

                        try:
                            conn.sendall(response)
                            log(f"Respuesta enviada ({len(response)} bytes).")
                        except Exception as e:
                            log(f"Error al enviar respuesta: {e}")
                            break

                        if interactivo:
                            log("Esperando ENTER para continuar...")
                            try:
                                input()
                            except KeyboardInterrupt:
                                log("Detención por teclado solicitada. Saliendo.")
                                raise

                        clear_screen()
                        log("Reiniciando ciclo de espera de requests...")

        except KeyboardInterrupt:
            log("Servidor detenido por teclado.")
        finally:
            log("Cerrando servidor.")
