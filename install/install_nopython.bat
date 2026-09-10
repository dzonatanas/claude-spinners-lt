@echo off
setlocal EnableDelayedExpansion

rem Pure-batch installer for spinnerVerbs -- no Python required.
rem
rem Usage:
rem   install_nopython.bat                          (global scope, replace mode)
rem   install_nopython.bat project                   (this directory, replace mode)
rem   install_nopython.bat project "C:\my\project"   (explicit project dir, replace mode)
rem   install_nopython.bat global append             (global scope, append mode)
rem
rem ASSUMPTION: an existing settings.json (if any) is standard pretty-printed
rem JSON (like Node's JSON.stringify(obj, null, 2)) with the root "}" as the
rem very last line and no blank lines inside. This covers every settings.json
rem Claude Code itself writes. If yours has been hand-edited with blank lines
rem or comments, use install.py instead (more robust) -- this script backs up
rem your file first regardless, so it's safe to try.
rem
rem NOTE: only ONE interactive prompt (a yes/no confirmation) is used, on
rem purpose -- cmd.exe's "set /p" is unreliable for a SECOND prompt later in
rem a script when input isn't a real interactive console (e.g. when piped for
rem testing), so scope/mode are taken from arguments or sensible defaults
rem instead of being asked one by one.
rem
rem Also: every "goto" here is a top-level statement, never nested inside a
rem parenthesized ( ) block, and no external "find.exe" call is used inside a
rem for /f command-capture (both are known cmd.exe fragility traps -- the
rem second one especially breaks when the script's own path contains spaces,
rem which this project's path does). Line skipping instead uses a "lag by one
rem line" print pattern that needs no line count at all.

set "SCRIPT_DIR=%~dp0"
set "VERBS_FILE=%SCRIPT_DIR%..\data\spinnerVerbs.settings.json"

set "MISSING_VERBS="
if not exist "%VERBS_FILE%" set "MISSING_VERBS=1"
if defined MISSING_VERBS goto :fail

set "SCOPE=global"
set "MODE=replace"
set "PROJ_DIR="

if /i "%~1"=="project" set "SCOPE=project"
if /i "%~1"=="global" set "SCOPE=global"
if /i "%~1"=="replace" set "MODE=replace"
if /i "%~1"=="append" set "MODE=append"
if /i "%~2"=="replace" set "MODE=replace"
if /i "%~2"=="append" set "MODE=append"
if /i "%~3"=="replace" set "MODE=replace"
if /i "%~3"=="append" set "MODE=append"

if /i "%SCOPE%"=="project" (
    set "PROJ_DIR=%~2"
    if "!PROJ_DIR!"=="" set "PROJ_DIR=%CD%"
    if /i "%~2"=="replace" set "PROJ_DIR=%CD%"
    if /i "%~2"=="append" set "PROJ_DIR=%CD%"
    set "TARGET=!PROJ_DIR!\.claude\settings.json"
) else (
    set "TARGET=%USERPROFILE%\.claude\settings.json"
)

echo Diegimo apzvalga:
echo   Apimtis (scope): %SCOPE%
if /i "%SCOPE%"=="project" echo   Projekto katalogas: !PROJ_DIR!
echo   Mode: %MODE%
echo   Tikslo failas: !TARGET!
echo.
echo Nera Python priklausomybiu -- viskas atliekama grynu batch tekstu.
echo Jei tikslo faile jau yra kitu nustatymu, jie NEBUS istrinti; failas bus
echo sujungtas, o originalas issaugotas kaip .bak prieš rasant.
echo.
set /p CONFIRM="Testi? (Y/n): "
if /i "%CONFIRM%"=="n" goto :cancelled

for %%F in ("!TARGET!") do set "TARGET_DIR=%%~dpF"
if not exist "!TARGET_DIR!" mkdir "!TARGET_DIR!" >nul 2>nul

set "TLINES=0"
set "NEED_FRESH="
if not exist "!TARGET!" (
    set "NEED_FRESH=1"
) else (
    echo Radau esama settings.json - darau atsargine kopija.
    "%SystemRoot%\System32\findstr.exe" /c:"spinnerVerbs" "!TARGET!" >nul 2>nul
    if not errorlevel 1 (
        echo DEMESIO: faile jau yra "spinnerVerbs" raktas. Sis skriptas nezino
        echo kaip pilnai issitrinti seno rakto teksto, tad prides NAUJA
        echo spinnerVerbs bloka po juo. JSON liks galiojantis ir naujausias
        echo blokas galios, bet jei nori svaraus failo, isvalyk sena blok^a
        echo rankiniu budu po sio veiksmo ^(originalas issaugotas .bak faile^).
        echo.
    )
    copy /y "!TARGET!" "!TARGET!.bak" >nul
    set "P1="
    set "P2="
    set "N=0"
    for /f "usebackq skip=1 delims=" %%L in ("!TARGET!") do (
        set /a N+=1
        if !N! GTR 2 (
            >> "!TARGET!.body" echo(!P2!
        )
        set "P2=!P1!"
        set "P1=%%L"
    )
    set "TLINES=!N!"
    if !TLINES! LSS 3 set "NEED_FRESH=1"
)

if defined NEED_FRESH (
    echo Nera esamo settings.json - kuriu nauja.
    type nul > "!TARGET!.body"
) else (
    rem P2 now holds the last real content line (e.g. the previous last key);
    rem give it a trailing comma if it doesn't already have one, and append it.
    set "LC=!P2:~-1!"
    if not "!LC!"=="," set "P2=!P2!,"
    >> "!TARGET!.body" echo(!P2!
)

rem Append the spinnerVerbs block: every VERBS_FILE line except its first
rem ("{") and its last ("}"), using the same lag-by-one pattern (skip=1
rem handles the first line, never-printing-the-final-PREV handles the last).
set "V1="
set "VN=0"
for /f "usebackq skip=1 delims=" %%B in ("%VERBS_FILE%") do (
    set /a VN+=1
    if !VN! GTR 1 (
        set "L=!V1!"
        if /i not "!MODE!"=="replace" set "L=!L:replace=append!"
        >> "!TARGET!.body" echo(!L!
    )
    set "V1=%%B"
)

rem The body already ends with the spinnerVerbs object's own closing "  }"
rem line (preserved from VERBS_FILE), so only the root "}" needs adding here.
(
    echo {
    type "!TARGET!.body"
    echo }
) > "!TARGET!.new"

del "!TARGET!.body"
move /y "!TARGET!.new" "!TARGET!" >nul

echo.
echo Sekmingai irasyta i: !TARGET!
echo mode: !MODE!
if not defined NEED_FRESH echo Jei kazkas atrodo sugadinta - originalas issaugotas kaip !TARGET!.bak
goto :end

:cancelled
echo Atsaukta, niekas nepakeista.
goto :end

:fail
echo Klaida: nerandu "%VERBS_FILE%" - paleisk sita faila is repo katalogo.

:end
echo.
pause
