; =========================================================
; Script: test_venta_carta_simple_son_smart_point.ahk
; Automatiza venta de carta simple con Smart Point
; =========================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
delayClickDefault := 200    ; Tiempo entre clics por defecto (ms)
delayShort := 100           ; Espera breve entre acciones (ms)
delayMedium := 1000         ; Espera media entre acciones (ms)
delayLong := 10000          ; Espera larga entre acciones (ms)
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
btnConfirmar_X := 650, btnConfirmar_Y := 500
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
btnConfirmarTicket_X := 950, btnConfirmarTicket_Y := 600
btnMenuAnterior_X := 270, btnMenuAnterior_Y := 470

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
Log("Inicio del test: Venta carta simple SON Smart Point")

; 0) Poner en foco la ventana principal si quedó tapada por el simulador
ClickBtn(btnFocoVentana_X, btnFocoVentana_Y, , "Foco ventana principal")

; 1) Identificar al cliente
ClickBtn(btnIdentificarCliente_X, btnIdentificarCliente_Y, , "Identificar cliente")
ClickBtn(btnDesplegarClientes_X, btnDesplegarClientes_Y, , "Desplegar clientes")
ClickBtn(btnSeleccionarCliente_X, btnSeleccionarCliente_Y, , "Seleccionar cliente")
Log("Se confirma el cliente.")
Send, {Enter}
ClickBtn(btnNoRequiereFactura_X, btnNoRequiereFactura_Y, , "No requiere factura")

; 2) Navegación de venta
ClickBtn(btnVentaOtros_X, btnVentaOtros_Y, , "Venta de otros servicios")
ClickBtn(btnPostalNacional_X, btnPostalNacional_Y, , "Postal Nacional")
ClickBtn(btnCartaSimple_X, btnCartaSimple_Y, , "Carta Simple")

; 3) Configuración de peso
ClickBtn(btnPesoCarta_X, btnPesoCarta_Y, , "Peso de la carta")
Send, {Del}
Sleep, %delayShort%
Send, %pesoCarta%
Sleep, %delayShort%
Send, {Enter}

; 4) Medios de pago
ClickBtn(btnConfirmar_X, btnConfirmar_Y, , "Confirmar venta")
ClickBtn(btnMediosPago_X, btnMediosPago_Y, , "Desplegar medios de pago")
ClickBtn(btnTarjetas_X, btnTarjetas_Y, , "Seleccionar tarjetas")
ClickBtn(btnMontoTarjeta_X, btnMontoTarjeta_Y, , "Monto tarjeta")
Send, %montoTarjeta%
Sleep, %delayShort%
Send, {Enter}

; 5) Mercado Pago
ClickBtn(btnCodigosInternos_X, btnCodigosInternos_Y, , "Códigos internos")
ClickBtn(btnMercadoPago_X, btnMercadoPago_Y, , "Mercado Pago")
ClickBtn(btnPointCredito_X, btnPointCredito_Y, , "Point Crédito")
ClickBtn(btnCodigoPlan_X, btnCodigoPlan_Y, , "Código de plan")
ClickBtn(btnPrimerPlan_X, btnPrimerPlan_Y, , "Primer plan")
ClickBtn(btnCuotas_X, btnCuotas_Y, , "Cuotas")
Send, %cuotasPago%
Sleep, %delayShort%
Send, {Enter}

; 6) Orden de pago
Sleep, %delayMedium%
Send, {Enter}
Sleep, %delayMedium%
Send, {Enter}
Sleep, %delayLong%

; 7) Resolución de impresión
ClickBtn(btnErrorImpresora_X, btnErrorImpresora_Y, , "Error de impresora")
ClickBtn(btnFocoVenta_X, btnFocoVenta_Y, , "Foco venta principal")
Log("Se confirma la operación.")
Send, {Enter}
ClickBtn(btnConfirmarTicket_X, btnConfirmarTicket_Y, , "Confirmar impresión")
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")

Log("Test finalizado correctamente.")
ExitApp
