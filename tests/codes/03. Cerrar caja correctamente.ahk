; =========================================================
; Script: 03. Cerrar caja correctamente.ahk
; Se ejecuta el cierre de caja correctamente con cambio de usuario
; =========================================================

CoordMode, Mouse, Screen

; --- CONFIGURACIÓN ---
waitPowerShell := 5000        ; Tiempo de espera al abrir PowerShell (ms)
waitDetectTerminal := 15000   ; Tiempo máximo de detección de terminal (ms)
waitAfterFirstRun := 10000    ; Tiempo de espera después de levantar consola (ms)
delayClickDefault := 200      ; Tiempo entre clics por defecto (ms)
delayMedium := 1000           ; Espera media entre acciones (ms)
logFile := "C:\moa_devtools\logs\test_log.txt"   ; Ruta del log

; --- COORDENADAS ---
btnAfip_X := 1124, btnAfip_Y := 605
btnCaja_X := 160, btnCaja_Y := 55

; --- FUNCIONES AUXILIARES ---

; Se registra un mensaje en el log
Log(msg) {
    global logFile
    FormatTime, timestamp,, yyyy-MM-dd HH:mm:ss
    FileAppend, [%timestamp%] %msg%`n, %logFile%
}

; Se hace clic con pausa y log
ClickBtn(x, y, delay := 0, label := "") {
    global delayClickDefault
    if (label != "")
        Log("Se hace clic en: " . label . " (" . x . "," . y . ")")
    Click, %x%, %y%
    Sleep, % (delay ? delay : delayClickDefault)
}

; Se envía un comando a PowerShell
SendPowerShellCommand(command, label := "") {
    global powerShellId, delayMedium
    if (powerShellId)
        WinActivate, ahk_id %powerShellId%
    if (label != "")
        Log(label)
    SendInput, %command%{Enter}
    Sleep, %delayMedium%
}

; Se obtiene un snapshot de ventanas de consola
GetConsoleWindowSnapshot() {
    snapshot := {}

    WinGet, consoleList, List, ahk_class ConsoleWindowClass
    Loop, %consoleList% {
        id := consoleList%A_Index%
        snapshot[id] := true
    }

    WinGet, wtList, List, ahk_class CASCADIA_HOSTING_WINDOW_CLASS
    Loop, %wtList% {
        id := wtList%A_Index%
        snapshot[id] := true
    }

    return snapshot
}

; Se espera la aparición de una nueva ventana de consola
WaitForNewConsoleWindow(snapshot, timeoutMs) {
    startTick := A_TickCount
    Loop {
        if ((A_TickCount - startTick) > timeoutMs)
            break

        WinGet, consoleList, List, ahk_class ConsoleWindowClass
        Loop, %consoleList% {
            id := consoleList%A_Index%
            if (!snapshot.HasKey(id))
                return id
        }

        WinGet, wtList, List, ahk_class CASCADIA_HOSTING_WINDOW_CLASS
        Loop, %wtList% {
            id := wtList%A_Index%
            if (!snapshot.HasKey(id))
                return id
        }

        Sleep, 250
    }
    return 0
}

; -----------------------
; --- INICIO DEL SCRIPT ---
; -----------------------

; Se crea la carpeta de logs si no existe
SplitPath, logFile, , logDir
FileCreateDir, %logDir%

Log("==============================================")
Log("Inicio del script: Cerrar caja correctamente")

; Paso 1: Se abre una ventana nueva de PowerShell y se configura USERNAME
Log("Se abre una ventana nueva de PowerShell.")
Run, powershell.exe
WinWaitActive, ahk_exe powershell.exe,, %waitPowerShell%
if (ErrorLevel) {
    Log("No se detectó la ventana de PowerShell.")
} else {
    WinGet, powerShellId, ID, A
    Log("Se detectó la ventana de PowerShell.")
}
SendPowerShellCommand("$env:USERNAME = ""ZEXTHCASTILLO""", "Se configura USERNAME en PowerShell (ZEXTHCASTILLO).")

; Paso 2 y 3: Se ejecuta rt -npost y se captura el PID de la terminal nueva
snapshot := GetConsoleWindowSnapshot()
SendPowerShellCommand("rt -npost", "Se ejecuta rt -npost.")
Log("Se espera la aparición de la terminal de log.")
logTerminalId := WaitForNewConsoleWindow(snapshot, waitDetectTerminal)
logTerminalPid := 0
if (logTerminalId) {
    WinGet, logTerminalPid, PID, ahk_id %logTerminalId%
    Log("Se capturó el PID de la terminal de log: " . logTerminalPid)
} else {
    Log("No se detectó la terminal de log dentro del tiempo esperado.")
}

Log("Se espera el inicio completo luego de la primera ejecución.")
Sleep, %waitAfterFirstRun%

; Paso 4: Cartel de AFIP
ClickBtn(btnAfip_X, btnAfip_Y, , "Cartel AFIP")

; Paso 5: Menú superior F2 Caja
ClickBtn(btnCaja_X, btnCaja_Y, , "F2 Caja")

; Paso 6: Se cierra la terminal de log capturada
if (logTerminalPid) {
    Log("Se intenta cerrar la terminal de log con PID: " . logTerminalPid)
    Process, Close, %logTerminalPid%
    Sleep, 500
    Process, Exist, %logTerminalPid%
    if (ErrorLevel) {
        Log("La terminal sigue activa, se fuerza el cierre.")
        RunWait, % "taskkill /PID " . logTerminalPid . " /T /F", , Hide
    } else {
        Log("Se cerró la terminal de log correctamente.")
    }
} else {
    Log("Se omite el cierre de terminal de log por falta de PID.")
}

; Paso 7: Se revierte USERNAME en PowerShell
SendPowerShellCommand("$env:USERNAME = ""NAHUMARTINEZ""", "Se configura USERNAME en PowerShell (NAHUMARTINEZ).")

; Paso 8: Se ejecuta nuevamente rt -npost
SendPowerShellCommand("rt -npost", "Se ejecuta rt -npost nuevamente.")

Log("Script finalizado correctamente.")

ExitApp
