"""
Constantes compartidas de configuración para MOA DevTools.
"""

import os


BASE_MOAPROJ = r"C:\moaproj"
RUTA_POST = os.path.join(BASE_MOAPROJ, "post")
RUTA_GIT = os.path.join(BASE_MOAPROJ, "Mosaic-gitlab")
RUTA_GIT_SRC = os.path.join(RUTA_GIT, "src")
RUTA_CDSGENE_POST = os.path.join(RUTA_POST, "cdsgene")
RUTA_CDSMAIN_POST = os.path.join(RUTA_POST, "cdsmain")
RUTA_CDSGENE_GIT = os.path.join(RUTA_GIT, "cdsgene")
RUTA_CDSMAIN_GIT = os.path.join(RUTA_GIT, "cdsmain")
RUTA_PASSWORD = os.path.join(BASE_MOAPROJ, "password")
RUTA_INIT_SUC = os.path.join(BASE_MOAPROJ, "scripts", "InitSuc")
RUTA_OPER_TEST = os.path.join(BASE_MOAPROJ, "scripts", "Oper_Test")

SERVICIOS = ["CDS_post01gene", "CDS_post01main", "RTBatch"]
ENV = "post"
SUCURSAL = "B0016"
