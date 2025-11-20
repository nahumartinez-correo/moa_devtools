"""
Define exclusivamente la lista de reemplazos generales.
Sin interpretar rutas, sin detectar versiones automáticamente,
sin procesar archivos. La única fuente de verdad es esta lista.
"""

def obtener_reemplazos_generales(version):

    base = f"C:\\moaproj\\{version}\\src\\INCLUDE"
    ofb  = "C:\\MOA\\src\\include\\ofb"

    return {
        '#include "drv.h"'         : f'#include "{base}\\drv.h"',
        '#include "ofbdefs.h"'     : f'#include "{base}\\ofbdefs.h"',
        '#include "keys.h"'        : f'#include "{base}\\keys.h"',
        '#include "presupuesto.h"' : f'#include "{base}\\presupuesto.h"',
        '#include "impresio.h"'    : f'#include "{base}\\impresio.h"',
        '#include "tesoro.h"'      : f'#include "{base}\\tesoro.h"',
        '#include "csr.h"'         : f'#include "{base}\\csr.h"',
        '#include <csr.h>'         : f'#include "{base}\\csr.h"',
        '#include "base.h"'        : f'#include "{base}\\base.h"',
        '#include "admin_dt.h"'     : f'#include "{base}\\admin_dt.h"',
        '#include "pickdrv.h"'     : f'#include "{base}\\pickdrv.h"',
        '#include "giros.h"'       : f'#include "{base}\\giros.h"',
        '#include "hcommstd.h"'    : f'#include "{base}\\hcommstd.h"',
        '#include "Sap.h"'         : f'#include "{base}\\Sap.h"',
        '#include "sap.h"'         : f'#include "{base}\\Sap.h"',
        '#include "sf1.h"'         : f'#include "{base}\\sf1.h"',
        '#include "sucuvirt.h"'    : f'#include "{base}\\sucuvirt.h"',
        '#include "commdef.h"'     : f'#include "{base}\\commdef.h"',
        '#include "descuento.h"'   : f'#include "{base}\\descuento.h"',
        '#include "bonif.h"'       : f'#include "{base}\\bonif.h"',
        '#include "reporte.h"'     : f'#include "{base}\\reporte.h"',
        '#include "postscr.h"'     : f'#include "C:\\moaproj\\{version}\\src\\POST\\scr\\postscr.h"',
        '#include "cdserdef.h"'    : f'#include "{ofb}\\cdserdef.h"',
        '#include "desktop.h"'     : f'#include "{ofb}\\desktop.h"',
        '#include "field.h"'       : f'#include "{ofb}\\field.h"',
        '#include "gsp.h"'         : f'#include "{base}\\gsp.h"',
        '#include "Hcommstd.h"'    : f'#include "{base}\\Hcommstd.h"',
        '#include "hcommstd.h"'    : f'#include "{base}\\Hcommstd.h"',
        '#include "HCOMMSTD.h"'    : f'#include "{base}\\Hcommstd.h"',
        '#include <hcommstd.h>'    : f'#include "{base}\\Hcommstd.h"',
        '#include "HCOMMSTD.H"'    : f'#include "{base}\\Hcommstd.h"',
        '#include "color.h"'       : f'#include "{base}\\color.h"',
    }
