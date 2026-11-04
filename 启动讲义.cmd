@echo off
setlocal
title Data Analysis - Interactive Textbook
chcp 65001 >nul
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
echo Starting the interactive textbook...
echo URL: http://127.0.0.1:8766
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found in PATH.
  echo Install Python 3.10+ and make sure "python" works in a new terminal.
  pause
  exit /b 1
)
python -X utf8 "%~dp0launch.py" %*
set "LECTURE_EXIT=%ERRORLEVEL%"
echo.
if not "%LECTURE_EXIT%"=="0" echo Startup failed. The details are shown above.
pause
exit /b %LECTURE_EXIT%
