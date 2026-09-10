@echo off
setlocal

rem Runs install.py from whatever directory this .bat file lives in,
rem so it works even if double-clicked from Explorer.
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
    python install.py %*
    goto :end
)

where py >nul 2>nul
if %errorlevel%==0 (
    py install.py %*
    goto :end
)

echo Klaida: nerastas Python. Idiek Python 3 is https://www.python.org/downloads/
echo ir paleisk sita faila is naujo.

:end
echo.
pause
