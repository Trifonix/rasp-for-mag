@echo off
REM Сборка курсовой: PDF + clean.txt, затем очистка временных файлов
setlocal EnableExtensions
cd /d "%~dp0"

if exist "%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" (
  set "PATH=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64;%PATH%"
)
if exist "%ProgramFiles%\MiKTeX\miktex\bin\x64\pdflatex.exe" (
  set "PATH=%ProgramFiles%\MiKTeX\miktex\bin\x64;%PATH%"
)

set "OUT_PDF=Trifonov_OSiBD_Course-2-work.pdf"
set "OUT_TXT=Trifonov_OSiBD_Course-2-work_clean.txt"

where pdflatex >nul 2>&1
if errorlevel 1 (
  echo Не найден pdflatex.
  echo Установите MiKTeX: https://miktex.org/download
  exit /b 1
)

echo ==^> Сборка PDF...
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if errorlevel 1 exit /b 1
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if errorlevel 1 exit /b 1

if not exist main.pdf (
  echo Ошибка: main.pdf не создан
  exit /b 1
)

copy /Y main.pdf "%OUT_PDF%" >nul

echo ==^> Текст для антиплагиата...
where python >nul 2>&1
if errorlevel 1 (
  echo Не найден python для export_clean.py
  exit /b 1
)
python export_clean.py "%OUT_TXT%"
if errorlevel 1 exit /b 1

echo ==^> Очистка временных файлов...
del /Q main.pdf main.aux main.log main.out main.toc main.synctex.gz 2>nul
del /Q clean.txt Trifonov_kursovaya_vizitka.pdf 2>nul
del /Q *.aux *.log *.out *.toc *.synctex.gz 2>nul

echo ==^> Готово:
echo     %CD%\%OUT_PDF%
echo     %CD%\%OUT_TXT%
endlocal
