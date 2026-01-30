; =========================================================
; Script: test_refund_operacion_simple_con_smart_point.ahk
; Refund de operación simple con Smart Point
; =========================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
appPath := "D:\MOA\BIN\rt.exe"
waitStartup := 10000          ; Tiempo de espera al iniciar (ms)
delayClickDefault := 200      ; Tiempo entre clics por defecto (ms)
delayShort := 200             ; Espera breve entre acciones (ms)
delayMedium := 1000         ; Espera media entre acciones (ms)
delayLong := 3000          ; Espera larga entre acciones (ms)
logFile := "C:\moa_devtools\logs\test_log.txt"   ; Ruta del log

; --- COORDENADAS ---
btnFocoVentana_X := 40, btnFocoVentana_Y := 250
btnMenuActividades_X := 470, btnMenuActividades_Y := 60
btnAnulacionDocs_X := 275, btnAnulacionDocs_Y := 385
btnDesplegarDocumentos_X := 780, btnDesplegarDocumentos_Y := 145
btnPrimerOperacion_X := 500, btnPrimerOperacion_Y := 190
btnPrimeraTransaccion_X := 50, btnPrimeraTransaccion_Y := 220
btnAceptarAnulacion_X := 1000, btnAceptarAnulacion_Y := 590
btnAceptarSupervision_X := 1000, btnAceptarSupervision_Y := 590
btnFocoVentanaPrincipal_X := 550, btnFocoVentanaPrincipal_Y := 450
btnConfirmarTicket_X := 950, btnConfirmarTicket_Y := 590
btnAceptarCaiVencido_X := 1050, btnAceptarCaiVencido_Y := 590
btnFocoVentanaPrincipal2_X := 20, btnFocoVentanaPrincipal2_Y := 100
btnConfirmarNotaCredito_X := 1000, btnConfirmarNotaCredito_Y := 590
btnMenuInicial_X := 300, btnMenuInicial_Y := 450
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
; --- INICIO DEL TEST ---
; -----------------------

; Crear carpeta de logs si no existe
SplitPath, logFile, , logDir
FileCreateDir, %logDir%

Log("==============================================")
Log("Inicio del test: Refund de operación simple con Smart Point")

; 1) Menú actividades
ClickBtn(btnMenuActividades_X, btnMenuActividades_Y, , "Menú actividades")

; 2) Anulación de documentos
ClickBtn(btnAnulacionDocs_X, btnAnulacionDocs_Y, , "Anulación de documentos")

; 3) Desplegar documentos
ClickBtn(btnDesplegarDocumentos_X, btnDesplegarDocumentos_Y, , "Desplegar documentos")

; 4) Seleccionar primera operación
ClickBtn(btnPrimerOperacion_X, btnPrimerOperacion_Y, , "Primera operación")

; 5) Seleccionar primera transacción
ClickBtn(btnPrimeraTransaccion_X, btnPrimeraTransaccion_Y, , "Primera transacción")

; 6) Confirmar operación
Send, {Enter}
Sleep, %delayShort%

; 7) Aceptar anulación de documentos
ClickBtn(btnAceptarAnulacion_X, btnAceptarAnulacion_Y, , "Aceptar anulación")

; 8) Aceptar supervisión de cajero
ClickBtn(btnAceptarSupervision_X, btnAceptarSupervision_Y, , "Aceptar supervisión")

; 9) Poner en foco nuevamente la ventana principal
ClickBtn(btnFocoVentanaPrincipal_X, btnFocoVentanaPrincipal_Y, , "Foco ventana principal")

; 10) Confirmar operación
Send, {Enter}
Sleep, %delayLong%

; 11) Confirmar impresión del ticket
ClickBtn(btnConfirmarTicket_X, btnConfirmarTicket_Y, , "Confirmar ticket")
Sleep, %delayMedium%

; 12) Aceptar CAI vencido
ClickBtn(btnAceptarCaiVencido_X, btnAceptarCaiVencido_Y, , "Aceptar CAI vencido")

; 13) Poner en foco nuevamente la ventana principal
ClickBtn(btnFocoVentanaPrincipal2_X, btnFocoVentanaPrincipal2_Y, , "Foco ventana principal")

; 14) Confirmar nota de crédito
Sleep, %delayMedium%
Sleep, %delayLong%
Sleep, %delayLong%
ClickBtn(btnConfirmarNotaCredito_X, btnConfirmarNotaCredito_Y, , "Confirmar nota de crédito")

; 15) Volver al menú inicial
ClickBtn(btnMenuInicial_X, btnMenuInicial_Y, , "Menú inicial")

; 16) Se aguarda que se actualice la interfaz
Sleep, %delayMedium%

; 17) Se hace click en Menú anterior
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")

; 18) Se hace click en Salir
ClickBtn(btnSalir_X, btnSalir_Y, , "Salir")

Log("==============================================")
Log("Test finalizado correctamente.")

ExitApp
