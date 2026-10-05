@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
python "0_parse-from/update_schedule.py" %*
echo.
pause
