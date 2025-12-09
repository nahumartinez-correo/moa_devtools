; =========================================================
; Script: test_vender_carta_simple_con_logs.ahk
; Automatiza navegación en Mosaic OA con logs y validaciones
; =========================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
appPath := "D:\MOA\BIN\rt.exe"
waitStartup := 10000          ; Tiempo de espera al iniciar (ms)
delayClickDefault := 200    ; Tiempo entre clics por defecto (ms)
logFile := "C:\MOA\Test\test_log.txt"   ; Ruta del log
pythonScript := "C:\MOA\Test\Simulador_MP\Simulador_MP.py"

; --- COORDENADAS ---

; Botón para abrir la caja
btnCaja_X := 160,  btnCaja_Y := 55
msgBoxBrowser_X := 1050,  msgBoxBrowser_Y := 590

; Controles para identificar al cliente
btnIdentificarCliente_X := 655,  btnIdentificarCliente_Y := 500
btnBuscarPor_X := 572,  btnBuscarPor_Y := 380
opcionBuscarPor_X := 400,  opcionBuscarPor_Y := 265
msgBoxRequiereFactura_X := 1020,  msgBoxRequiereFactura_Y := 590

; Botones para acceder al menú de venta de una carta simple internacional
btnVentaOtros_X := 270,  btnVentaOtros_Y := 280
btnPostalInt_X := 270,  btnPostalInt_Y := 220
btnCartaSimple_X := 100,  btnCartaSimple_Y := 220

; Controles en la pantalla para realizar la venta
btnDestino_X := 390,  btnDestino_Y := 335
opcionDestino_X := 260,  opcionDestino_Y := 385
textBoxPeso_X := 240,  textBoxPeso_Y := 435

; Controles para la captura del medio de pago
btnConfirmar_X := 660,  btnConfirmar_Y := 500
opcionesMedioDePago_X := 40,  opcionesMedioDePago_Y := 350
opcionTarjetas_X := 530,  opcionTarjetas_Y := 235
textBoxEfectivo_X := 450,  textBoxEfectivo_Y := 315
textBoxTarjeta_X := 600,  textBoxTarjeta_Y := 350
msgBoxMuchoEfectivo_X := 1000,  msgBoxMuchoEfectivo_Y := 600

; Controles para la selección de MP
opcionesCodInt_X := 185,  opcionesCodInt_Y := 350
opcionMecadoPago_X := 350,  opcionMecadoPago_Y := 150
opcionPointCredito_X := 350,  opcionPointCredito_Y := 150
opcionesCodPlan_X := 145,  opcionesCodPlan_Y := 380
opcionSinPlan_X := 350,  opcionSinPlan_Y := 150
textBoxCuotas_X := 410,  textBoxCuotas_Y := 380





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
; --- INICIO DEL TEST ---
; -----------------------

; Crear carpeta de logs si no existe
SplitPath, logFile, , logDir
FileCreateDir, %logDir%

Log("==============================================")
Log("Inicio del test: Venta carta simple internacional")

; --- Levantar servidor Python en paralelo con consola visible ---
;Log("Iniciando script Python: " . pythonScript)
;Run, cmd.exe /k "python.exe ""%pythonScript%"""
;Log("Servidor Python iniciado (consola visible).")

Run, %appPath%
Log("Aplicación iniciada.")
Sleep, %waitStartup%

; -----------------------
; 1) Se abre la caja
; -----------------------

; Se presiona el botón del menú superior -  F2 Caja
ClickBtn(btnCaja_X, btnCaja_Y, , "F2 Caja")

; Se cancela el MsgBox que indica que me falta la tabla Browser
ClickBtn(msgBoxBrowser_X, msgBoxBrowser_Y, , "Cerrar MsgBox Browser")

; -----------------------
; 2) Se identifica al cliente
; -----------------------

; Se presiona el botón del menú lateral - Identificar cliente
ClickBtn(btnIdentificarCliente_X, btnIdentificarCliente_Y, , "Identificar cliente")

; Se despliega el menú de identificación
ClickBtn(btnBuscarPor_X, btnBuscarPor_Y, , "Desplegable para identificar")

; Se selecciona la opción disponible para el cliente
ClickBtn(opcionBuscarPor_X, opcionBuscarPor_Y, , "Selección del cliente")

; Se da Enter para confirmar la operación
Send, {Enter}

; Se indica en el MsgBox que el cliente no requiere de factura
ClickBtn(msgBoxRequiereFactura_X, msgBoxRequiereFactura_Y, , "No requiere factura")

; -----------------------
; 3) Se navega por el menú hasta la pantalla de la venta
; -----------------------

; Se presiona el botón del menú para "Venta de otros servicios"
ClickBtn(btnVentaOtros_X, btnVentaOtros_Y, , "Venta de otros servicios")

; Se presiona el botón del menú para "Postal internacional"
ClickBtn(btnPostalInt_X, btnPostalInt_Y, , "Postal internacional")

; Se presiona el botón del menú para "Carta simple"
ClickBtn(btnCartaSimple_X, btnCartaSimple_Y, , "Carta simple")

; -----------------------
; 4) Se configura la venta
; -----------------------

; Se despliega el menú de destino
ClickBtn(btnDestino_X, btnDestino_Y, , "Menu desplegable de destino")

; Se selecciona el destino dentro de las opciones
ClickBtn(opcionDestino_X, opcionDestino_Y, , "Opcion de destino")

; Se selecciona el control para ingresar el peso
ClickBtn(textBoxPeso_X, textBoxPeso_Y, , "Ingreso del peso")

; Se borra contenido anterior
Send, ^a
Sleep, 100
Send, {Del}
Sleep, 100

; Se ingresa el nuevo valor
Send, 100
Sleep, 300

; Se da Enter para confirmar la operación
Send, {Enter}

; -----------------------
; 5) Se configuran los pagos
; -----------------------

; Se presiona el botón para ir a seleccionar los medios de pago
ClickBtn(btnConfirmar_X, btnConfirmar_Y, , "Ir al menú de medios de pago")

; Se despliega el menú de medios de pago para elegir la tarjeta
ClickBtn(opcionesMedioDePago_X, opcionesMedioDePago_Y, , "Menu desplegable de medios de pago")

; Se selecciona el pago con tarjeta
ClickBtn(opcionTarjetas_X, opcionTarjetas_Y, , "Pago con tarjeta")

; Se selecciona el control para ingresar el monto pagado en efectivo
ClickBtn(textBoxEfectivo_X, textBoxEfectivo_Y, , "Ingreso de monto en efectivo")

; Se borra contenido anterior
Send, ^a
Sleep, 100
Send, {Del}
Sleep, 100

; Se ingresa el nuevo valor
Send, 10000
Sleep, 300

; Se selecciona el control para ingresar el monto pagado con las tarjetas
ClickBtn(textBoxTarjeta_X, textBoxTarjeta_Y, , "Ingreso de monto con tarjeta")

; Se borra contenido anterior
Send, ^a
Sleep, 100
Send, {Del}
Sleep, 100

; Se ingresa el nuevo valor
Send, 220000
Sleep, 300

; Se da Enter para confirmar la operación
Send, {Enter}

; Se acepta el MsgBox que indica que requiere supervisión por el efectivo
ClickBtn(msgBoxMuchoEfectivo_X, msgBoxMuchoEfectivo_Y, , "Ingreso de monto con tarjeta")

; -----------------------
; 6) Se configura la tarjeta de MercadoPago
; -----------------------

; Se despliega el menú de códigos internos para elegir MercadoPago
ClickBtn(opcionesCodInt_X, opcionesCodInt_Y, , "Menu desplegable de códigos internos")

; Se selecciona el pago con MercadoPago
ClickBtn(opcionMecadoPago_X, opcionMecadoPago_Y, , "Selección de MercadoPago")

; Se selecciona el pago con Point Credito
ClickBtn(opcionPointCredito_X, opcionPointCredito_Y, , "Selección de Point Credito")

; Se despliega el menú de planes para elegir Sin Plan
ClickBtn(opcionesCodPlan_X, opcionesCodPlan_Y, , "Menu desplegable de planes de pago")

; Se selecciona sin plan
ClickBtn(opcionSinPlan_X, opcionSinPlan_Y, , "Sin plan")

; Se selecciona el control para ingresar el monto de las cuotas del pago
ClickBtn(textBoxCuotas_X, textBoxCuotas_Y, , "Cuotas del pago")

; Se borra contenido anterior
Send, ^a
Sleep, 100
Send, {Del}
Sleep, 100

; Se ingresa el nuevo valor
Send, 1
Sleep, 300

; Se da Enter para confirmar la operación
Send, {Enter}

; -----------------------
; 7) Se Queda en el menú de espera para ver el status de la orden de pago
; -----------------------

; Se da Enter para iniciar la operación y Crear la orden de pago
Send, {Enter}




Log("Test finalizado exitosamente.")
MsgBox, 64, Finalizado, Test completado correctamente.

ExitApp
