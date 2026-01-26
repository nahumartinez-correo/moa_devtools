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
logFile := "C:\moa_devtools\logs\test_log.txt"   ; Ruta del log

; --- COORDENADAS ---
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

; 1) Levantar Mosaic
Run, %appPath%
Log("Aplicación iniciada.")
Sleep, %waitStartup%

; 2) Menú actividades
ClickBtn(btnMenuActividades_X, btnMenuActividades_Y, , "Menú actividades")

; 3) Anulación de documentos
ClickBtn(btnAnulacionDocs_X, btnAnulacionDocs_Y, , "Anulación de documentos")

; 4) Desplegar documentos
ClickBtn(btnDesplegarDocumentos_X, btnDesplegarDocumentos_Y, , "Desplegar documentos")

; 5) Seleccionar primera operación
ClickBtn(btnPrimerOperacion_X, btnPrimerOperacion_Y, , "Primera operación")

; 6) Seleccionar primera transacción
ClickBtn(btnPrimeraTransaccion_X, btnPrimeraTransaccion_Y, , "Primera transacción")

; 7) Confirmar operación
Send, {Enter}
Sleep, %delayShort%

; 8) Aceptar anulación de documentos
ClickBtn(btnAceptarAnulacion_X, btnAceptarAnulacion_Y, , "Aceptar anulación")

; 9) Aceptar supervisión de cajero
ClickBtn(btnAceptarSupervision_X, btnAceptarSupervision_Y, , "Aceptar supervisión")

; 10) Poner en foco nuevamente la ventana principal
ClickBtn(btnFocoVentanaPrincipal_X, btnFocoVentanaPrincipal_Y, , "Foco ventana principal")

; 11) Confirmar operación
Send, {Enter}
Sleep, %delayShort%

; 12) Confirmar impresión del ticket
ClickBtn(btnConfirmarTicket_X, btnConfirmarTicket_Y, , "Confirmar ticket")

; 13) Aceptar CAI vencido
ClickBtn(btnAceptarCaiVencido_X, btnAceptarCaiVencido_Y, , "Aceptar CAI vencido")

; 14) Poner en foco nuevamente la ventana principal
ClickBtn(btnFocoVentanaPrincipal2_X, btnFocoVentanaPrincipal2_Y, , "Foco ventana principal")

; 15) Confirmar nota de crédito
ClickBtn(btnConfirmarNotaCredito_X, btnConfirmarNotaCredito_Y, , "Confirmar nota de crédito")

; 16) Volver al menú inicial
ClickBtn(btnMenuInicial_X, btnMenuInicial_Y, , "Menú inicial")

Log("Test finalizado correctamente.")
ExitApp
