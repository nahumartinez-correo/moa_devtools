; =========================================================
; Script: test_operacion_simple_y_refund_con_smart_point.ahk
; Se automatiza operación simple y refund con Smart Point
; =========================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
appPath := "D:\MOA\BIN\rt.exe"
waitStartup := 10000          ; Tiempo de espera al iniciar (ms)
delayClickDefault := 200      ; Tiempo entre clics por defecto (ms)
delayShortVenta := 100        ; Espera breve entre acciones (ms)
delayMediumVenta := 1000      ; Espera media entre acciones (ms)
delayLongVenta := 10000       ; Espera larga entre acciones (ms)
delayShortRefund := 200       ; Espera breve entre acciones (ms)
delayMediumRefund := 1000     ; Espera media entre acciones (ms)
delayLongRefund := 3000       ; Espera larga entre acciones (ms)
delayMedium := 1000           ; Espera media entre acciones (ms)
logFile := "C:\moa_devtools\logs\test_log.txt"   ; Ruta del log

pesoCarta := 20
montoTarjeta := 210000
cuotasPago := 1

; --- COORDENADAS ---
btnIdentificarCliente_X := 660, btnIdentificarCliente_Y := 500
btnDesplegarClientes_X := 575, btnDesplegarClientes_Y := 380
btnSeleccionarCliente_X := 300, btnSeleccionarCliente_Y := 265
btnNoRequiereFactura_X := 1030, btnNoRequiereFactura_Y := 590
btnVentaOtros_X := 270, btnVentaOtros_Y := 290
btnPostalNacional_X := 110, btnPostalNacional_Y := 240
btnCartaSimple_X := 110, btnCartaSimple_Y := 240
btnPesoCarta_X := 250, btnPesoCarta_Y := 450
btnConfirmarVenta_X := 650, btnConfirmarVenta_Y := 500
btnMediosPago_X := 40, btnMediosPago_Y := 350
btnTarjetas_X := 550, btnTarjetas_Y := 220
btnMontoTarjeta_X := 600, btnMontoTarjeta_Y := 350
btnFocoVentana_X := 40, btnFocoVentana_Y := 250
btnCodigosInternos_X := 180, btnCodigosInternos_Y := 350
btnMercadoPago_X := 400, btnMercadoPago_Y := 150
btnPointCredito_X := 400, btnPointCredito_Y := 150
btnCodigoPlan_X := 145, btnCodigoPlan_Y := 380
btnPrimerPlan_X := 400, btnPrimerPlan_Y := 150
btnCuotas_X := 415, btnCuotas_Y := 380
btnErrorImpresora_X := 1050, btnErrorImpresora_Y := 600
btnFocoVenta_X := 450, btnFocoVenta_Y := 350
btnConfirmarTicketVenta_X := 950, btnConfirmarTicketVenta_Y := 600
btnMenuAnterior_X := 270, btnMenuAnterior_Y := 470
btnSalir_X := 700, btnSalir_Y := 550
btnMenuActividades_X := 470, btnMenuActividades_Y := 60
btnAnulacionDocs_X := 275, btnAnulacionDocs_Y := 385
btnDesplegarDocumentos_X := 780, btnDesplegarDocumentos_Y := 145
btnPrimerOperacion_X := 500, btnPrimerOperacion_Y := 190
btnPrimeraTransaccion_X := 50, btnPrimeraTransaccion_Y := 220
btnAceptarAnulacion_X := 1000, btnAceptarAnulacion_Y := 590
btnAceptarSupervision_X := 1000, btnAceptarSupervision_Y := 590
btnFocoVentanaPrincipal_X := 550, btnFocoVentanaPrincipal_Y := 450
btnConfirmarTicketRefund_X := 950, btnConfirmarTicketRefund_Y := 590
btnAceptarCaiVencido_X := 1050, btnAceptarCaiVencido_Y := 590
btnFocoVentanaPrincipal2_X := 20, btnFocoVentanaPrincipal2_Y := 100
btnConfirmarNotaCredito_X := 1000, btnConfirmarNotaCredito_Y := 590
btnMenuInicial_X := 300, btnMenuInicial_Y := 450

; --- FUNCIONES AUXILIARES ---

; Se registra mensaje en el log
Log(msg) {
    global logFile
    FormatTime, timestamp,, yyyy-MM-dd HH:mm:ss
    FileAppend, [%timestamp%] %msg%`n, %logFile%
}

; Se hace clic con pausa y log
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

; Se crea carpeta de logs si no existe
SplitPath, logFile, , logDir
FileCreateDir, %logDir%

Log("==============================================")
Log("Inicio del test: Operación simple y refund con Smart Point")

; 0) Se pone en foco la ventana principal si quedó tapada por el simulador
ClickBtn(btnFocoVentana_X, btnFocoVentana_Y, , "Foco ventana principal")

; 1) Se identifica al cliente
ClickBtn(btnIdentificarCliente_X, btnIdentificarCliente_Y, , "Identificar cliente")
ClickBtn(btnDesplegarClientes_X, btnDesplegarClientes_Y, , "Desplegar clientes")
ClickBtn(btnSeleccionarCliente_X, btnSeleccionarCliente_Y, , "Seleccionar cliente")
Log("Se confirma el cliente.")
Send, {Enter}
ClickBtn(btnNoRequiereFactura_X, btnNoRequiereFactura_Y, , "No requiere factura")

; 2) Se navega en venta
ClickBtn(btnVentaOtros_X, btnVentaOtros_Y, , "Venta de otros servicios")
ClickBtn(btnPostalNacional_X, btnPostalNacional_Y, , "Postal Nacional")
ClickBtn(btnCartaSimple_X, btnCartaSimple_Y, , "Carta Simple")

; 3) Se configura el peso
ClickBtn(btnPesoCarta_X, btnPesoCarta_Y, , "Peso de la carta")
Send, {Del}
Sleep, %delayShortVenta%
Send, %pesoCarta%
Sleep, %delayShortVenta%
Send, {Enter}

; 4) Se configuran medios de pago
ClickBtn(btnConfirmarVenta_X, btnConfirmarVenta_Y, , "Confirmar venta")
ClickBtn(btnMediosPago_X, btnMediosPago_Y, , "Desplegar medios de pago")
ClickBtn(btnTarjetas_X, btnTarjetas_Y, , "Seleccionar tarjetas")
ClickBtn(btnMontoTarjeta_X, btnMontoTarjeta_Y, , "Monto tarjeta")
Send, %montoTarjeta%
Sleep, %delayShortVenta%
Send, {Enter}

; 5) Se selecciona Mercado Pago
ClickBtn(btnCodigosInternos_X, btnCodigosInternos_Y, , "Códigos internos")
ClickBtn(btnMercadoPago_X, btnMercadoPago_Y, , "Mercado Pago")
ClickBtn(btnPointCredito_X, btnPointCredito_Y, , "Point Crédito")
ClickBtn(btnCodigoPlan_X, btnCodigoPlan_Y, , "Código de plan")
ClickBtn(btnPrimerPlan_X, btnPrimerPlan_Y, , "Primer plan")
ClickBtn(btnCuotas_X, btnCuotas_Y, , "Cuotas")
Send, %cuotasPago%
Sleep, %delayShortVenta%
Send, {Enter}

; 6) Se confirma la orden de pago
Sleep, %delayMediumVenta%
Send, {Enter}
Sleep, %delayMediumVenta%
Send, {Enter}
Sleep, %delayLongVenta%
Sleep, %delayMediumVenta%
Sleep, %delayMediumVenta%

; 7) Se resuelve la impresión
ClickBtn(btnErrorImpresora_X, btnErrorImpresora_Y, , "Error de impresora")
ClickBtn(btnFocoVenta_X, btnFocoVenta_Y, , "Foco venta principal")
Log("Se confirma la operación.")
Send, {Enter}
ClickBtn(btnConfirmarTicketVenta_X, btnConfirmarTicketVenta_Y, , "Confirmar impresión")
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")

Sleep, 1000
Log("Se inicia el refund de la operación simple.")

; 8) Se ingresa al menú actividades
ClickBtn(btnMenuActividades_X, btnMenuActividades_Y, , "Menú actividades")

; 9) Se ingresa a anulación de documentos
ClickBtn(btnAnulacionDocs_X, btnAnulacionDocs_Y, , "Anulación de documentos")

; 10) Se despliegan documentos
ClickBtn(btnDesplegarDocumentos_X, btnDesplegarDocumentos_Y, , "Desplegar documentos")

; 11) Se selecciona la primera operación
ClickBtn(btnPrimerOperacion_X, btnPrimerOperacion_Y, , "Primera operación")

; 12) Se selecciona la primera transacción
ClickBtn(btnPrimeraTransaccion_X, btnPrimeraTransaccion_Y, , "Primera transacción")

; 13) Se confirma la operación
Send, {Enter}
Sleep, %delayShortRefund%

; 14) Se acepta la anulación de documentos
ClickBtn(btnAceptarAnulacion_X, btnAceptarAnulacion_Y, , "Aceptar anulación")

; 15) Se acepta la supervisión de cajero
ClickBtn(btnAceptarSupervision_X, btnAceptarSupervision_Y, , "Aceptar supervisión")

; 16) Se pone en foco nuevamente la ventana principal
ClickBtn(btnFocoVentanaPrincipal_X, btnFocoVentanaPrincipal_Y, , "Foco ventana principal")

; 17) Se confirma la operación
Send, {Enter}
Sleep, %delayLongRefund%

; 18) Se confirma la impresión del ticket
ClickBtn(btnConfirmarTicketRefund_X, btnConfirmarTicketRefund_Y, , "Confirmar ticket")

; 19) Se pone en foco nuevamente la ventana principal
ClickBtn(btnFocoVentanaPrincipal2_X, btnFocoVentanaPrincipal2_Y, , "Foco ventana principal")

; 20) Se acepta CAI vencido
Sleep, %delayMediumRefund%
ClickBtn(btnAceptarCaiVencido_X, btnAceptarCaiVencido_Y, , "Aceptar CAI vencido")
Sleep, %delayMediumRefund%

; 21) Se pone en foco nuevamente la ventana principal
ClickBtn(btnFocoVentanaPrincipal2_X, btnFocoVentanaPrincipal2_Y, , "Foco ventana principal")

; 22) Se confirma la nota de crédito
Sleep, %delayLongRefund%
ClickBtn(btnConfirmarNotaCredito_X, btnConfirmarNotaCredito_Y, , "Confirmar nota de crédito")

; 23) Se vuelve al menú inicial
ClickBtn(btnMenuInicial_X, btnMenuInicial_Y, , "Menú inicial")

Log("Test finalizado correctamente.")

btnMenuAnterior_X := 280, btnMenuAnterior_Y := 450

; 24) Se aguarda que se actualice la interfaz
Sleep, %delayMedium%

; 25) Se hace click en Menú anterior
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")

; 26) Se hace click en Salir
ClickBtn(btnSalir_X, btnSalir_Y, , "Salir")

ExitApp
