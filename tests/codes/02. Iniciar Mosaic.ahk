; =========================================================
; Script: 02. Iniciar Mosaic.ahk
; Inicializa Mosaic, espera el arranque y abre la caja
; =========================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
appPath := "D:\MOA\BIN\rt.exe"
waitStartup := 10000          ; Tiempo de espera al iniciar (ms)
waitAfterStart := 3000        ; Tiempo de espera tras abrir caja (ms)
delayClickDefault := 200      ; Tiempo entre clics por defecto (ms)
delayMedium := 1000           ; Espera media entre acciones (ms)
logFile := "C:\moa_devtools\logs\test_log.txt"   ; Ruta del log

; --- COORDENADAS ---
btnAfip_X := 1124,  btnAfip_Y := 605
btnCaja_X := 160,  btnCaja_Y := 55
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
Log("Inicio del script: Iniciar Mosaic")

Run, %appPath%
Log("Aplicación iniciada.")
Sleep, %waitStartup%

; 3) Cartel de AFIP
ClickBtn(btnAfip_X, btnAfip_Y, , "Cartel AFIP")

; Se presiona el botón del menú superior - F2 Caja
ClickBtn(btnCaja_X, btnCaja_Y, , "F2 Caja")

Sleep, %waitAfterStart%

Log("Script finalizado correctamente.")

; 23) Se aguarda que se actualice la interfaz
Sleep, %delayMedium%

; 24) Se hace click en Menú anterior
ClickBtn(btnMenuAnterior_X, btnMenuAnterior_Y, , "Menú anterior")

; 25) Se hace click en Salir
ClickBtn(btnSalir_X, btnSalir_Y, , "Salir")

ExitApp
