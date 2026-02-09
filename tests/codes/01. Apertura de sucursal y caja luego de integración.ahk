; =====================================================================
; Script: 01. Apertura de sucursal y caja luego de integración.ahk
; Automatiza la apertura inicial de sucursal y caja luego de integración
; =====================================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
rtCommand := "rt -npost -c"
waitStartup := 10000          ; Tiempo de espera al iniciar (ms)
waitPostMensajes := 5000      ; Tiempo de espera después de mensajes (ms)
delayClickDefault := 200      ; Tiempo entre clics por defecto (ms)
delayMedium := 1000           ; Espera media entre acciones (ms)
logFile := "C:\moa_devtools\logs\test_log.txt"   ; Ruta del log

; --- COORDENADAS ---
btnAfip_X := 1124, btnAfip_Y := 605
btnSucursal_X := 433, btnSucursal_Y := 70
btnCancelarNoLinea_X := 1076, btnCancelarNoLinea_Y := 593
btnAceptarNoHost_X := 1078, btnAceptarNoHost_Y := 606
btnAceptarPiezasPendientes_X := 1170, btnAceptarPiezasPendientes_Y := 598
btnAceptarDatos_X := 1146, btnAceptarDatos_Y := 596
btnAceptarAperturaManual_X := 1052, btnAceptarAperturaManual_Y := 589
btnAceptarScriptSinHost_X := 1100, btnAceptarScriptSinHost_Y := 600
btnFocoVentana_X := 600, btnFocoVentana_Y := 250
btnCaja_X := 150, btnCaja_Y := 60
btnMenuAnterior_X := 280, btnMenuAnterior_Y := 450
btnSalir_X := 700, btnSalir_Y := 550

; --- FUNCIONES AUXILIARES ---

; Registrar mensaje en el log
Log(msg) {
    global logFile
    FormatTime, timestamp,, yyyy-MM-dd HH:mm:ss
    FileAppend, [%timestamp%] %msg%`n, %logFile%
}

; Clic con pausa y log
ClickBtn(x, y, delay := 0, label := "") {
    global delayClickDefault
    if (label != "")
        Log("Clic en: " . label . " (" . x . "," . y . ")")
    Click, %x%, %y%
    Sleep, % (delay ? delay : delayClickDefault)
}

; -----------------------
; --- INICIO DEL SCRIPT ---
; -----------------------

; Crear carpeta de logs si no existe
SplitPath, logFile, , logDir
FileCreateDir, %logDir%

Log("==============================================")
Log("Inicio del script: Apertura de sucursal y caja luego de integración")

; 1) Levantar el RT sin conexión desde una terminal
Log("Se inicia el RT sin conexión.")
Run, cmd.exe /c "%rtCommand%"
Sleep, %waitStartup%

; 3) Cartel de AFIP
ClickBtn(btnAfip_X, btnAfip_Y, , "Cartel AFIP")

; 4) Botón de Sucursal
ClickBtn(btnSucursal_X, btnSucursal_Y, , "Botón Sucursal")

; 5) Confirmación
Log("Se confirma la selección de sucursal.")
Send, {Enter}

; 6) Cancelar "No hay línea"
ClickBtn(btnCancelarNoLinea_X, btnCancelarNoLinea_Y, , "Cancelar No hay línea")

; 7) Aceptar "No hay Host"
ClickBtn(btnAceptarNoHost_X, btnAceptarNoHost_Y, , "Aceptar No hay Host")

; 8) Aceptar actualización de piezas pendientes
ClickBtn(btnAceptarPiezasPendientes_X, btnAceptarPiezasPendientes_Y, , "Aceptar actualización piezas pendientes")

; 9) Cancelar "No hay línea"
ClickBtn(btnCancelarNoLinea_X, btnCancelarNoLinea_Y, , "Cancelar No hay línea")

; 10) Aceptar "No hay Host"
ClickBtn(btnAceptarNoHost_X, btnAceptarNoHost_Y, , "Aceptar No hay Host")

; 11) Aceptar actualización de datos
ClickBtn(btnAceptarDatos_X, btnAceptarDatos_Y, , "Aceptar actualización de datos")

; 12) Esperar mensajes finales
Sleep, %waitPostMensajes%

; 13) Aceptar apertura manual
ClickBtn(btnAceptarAperturaManual_X, btnAceptarAperturaManual_Y, , "Aceptar apertura manual")

; 14) Confirmación
Log("Se confirma la apertura manual.")
Send, {Enter}

; 15) Aceptar "Recurso de Host de scripts no configurado"
ClickBtn(btnAceptarScriptSinHost_X, btnAceptarScriptSinHost_Y, , "Aceptar scripts sin host")

; 16) Aceptar "Sin respuesta del servidor de scripts"
ClickBtn(btnAceptarScriptSinHost_X, btnAceptarScriptSinHost_Y, , "Aceptar sin respuesta servidor de scripts")

; 17) Aceptar "Recurso de Host de scripts no configurado"
ClickBtn(btnAceptarScriptSinHost_X, btnAceptarScriptSinHost_Y, , "Aceptar scripts sin host")

; 18) Aceptar "Sin respuesta del servidor de scripts"
ClickBtn(btnAceptarScriptSinHost_X, btnAceptarScriptSinHost_Y, , "Aceptar sin respuesta servidor de scripts")

; 19) Poner en foco la ventana principal
ClickBtn(btnFocoVentana_X, btnFocoVentana_Y, , "Foco ventana principal")

; 20) Salir de pantalla modal si aplica
Log("Se envía Escape para limpiar pantalla.")
Send, {Esc}

; 21) Botón de Caja
ClickBtn(btnCaja_X, btnCaja_Y, , "Botón Caja")

; 22) Confirmación final
Log("Se confirma la apertura de caja.")
Send, {Enter}

; 23) Se aguarda que se actualice la interfaz
Sleep, %delayMedium%

; 24) Se hace click en Menú anterior
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")

; 25) Se hace click en Salir
ClickBtn(btnSalir_X, btnSalir_Y, , "Salir")

ExitApp
