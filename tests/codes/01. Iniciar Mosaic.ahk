; =========================================================
; Script: 01. Iniciar Mosaic.ahk
; Inicializa Mosaic, espera el arranque y abre la caja
; =========================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
appPath := "D:\MOA\BIN\rt.exe"
waitStartup := 10000          ; Tiempo de espera al iniciar (ms)
delayClickDefault := 200      ; Tiempo entre clics por defecto (ms)
logFile := "C:\moa_devtools\logs\test_log.txt"   ; Ruta del log

; --- COORDENADAS ---
btnCaja_X := 160,  btnCaja_Y := 55

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
Log("Inicio del script: Iniciar Mosaic")

Run, %appPath%
Log("Aplicación iniciada.")
Sleep, %waitStartup%

; Se presiona el botón del menú superior - F2 Caja
ClickBtn(btnCaja_X, btnCaja_Y, , "F2 Caja")

Log("Script finalizado correctamente.")
MsgBox, 64, Finalizado, Mosaic iniciado y caja abierta correctamente.

ExitApp
