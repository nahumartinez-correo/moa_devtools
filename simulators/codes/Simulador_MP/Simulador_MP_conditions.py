# --------------------------------------------------------------
# Simulador_MP_conditions.py
# Tabla centralizada de condiciones simulables.
# Cada condición define cómo debe variar el campo 39 y
# qué campos adicionales deben generarse.
# --------------------------------------------------------------

CONDITIONS = {
    "server_down": {
        "descripcion": "Simula caída del servidor backend",
        "codigo_39": "96",
        "usa_105": True,
        "usa_106": False,
        "usa_107": False,
    },

    "rechazo_operador": {
        "descripcion": "Simula rechazo por parte del operador",
        "codigo_39": "05",
        "usa_105": True,
        "usa_106": True,
        "usa_107": False,
    },

    "request_Refund_ya_completado_anteriormente": {
        "descripcion": "Simula nuevo request de un Refund completado anteriormente",
        "codigo_39": "00",
        "usa_105": True,
        "usa_106": True,
        "usa_107": False,
    },
}
