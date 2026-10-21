@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PY=python"
if exist "%~dp0venv\Scripts\python.exe" set "PY=%~dp0venv\Scripts\python.exe"
"%PY%" testar_plataformas.py %*
pause
