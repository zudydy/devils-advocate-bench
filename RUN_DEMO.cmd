@echo off
setlocal
cd /d "%~dp0"
set "DA_BENCH_PY=python"
if exist "%USERPROFILE%\miniconda3\python.exe" set "DA_BENCH_PY=%USERPROFILE%\miniconda3\python.exe"
"%DA_BENCH_PY%" benchmark.py validate
if errorlevel 1 goto failed
"%DA_BENCH_PY%" benchmark.py demo
if errorlevel 1 goto failed
"%DA_BENCH_PY%" -m unittest -v
if errorlevel 1 goto failed
echo.
echo Done. Open results\demo\always_challenge.html and reviewer.html.
pause
exit /b 0
:failed
echo Failed. Check the message above. Python 3.10 or later is required.
pause
exit /b 1
