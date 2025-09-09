@echo off
REM ============================================================
REM Recriar_EXE.bat - cria venv, instala libs e gera EXE
REM Execute com duplo clique na pasta do projeto
REM ============================================================

setlocal ENABLEDELAYEDEXPANSION

echo =============================
echo 1) Limpando builds anteriores
echo =============================
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist JHervilha_Contas.spec del /q JHervilha_Contas.spec

echo.
echo =============================
echo 2) Criando/ativando venv .venv
echo =============================
if not exist ".venv" (
    py -3 -m venv .venv
)
call .venv\Scripts\activate

echo.
echo =============================
echo 3) Atualizando pip e instalando dependências
echo =============================
python -m pip install --upgrade pip
pip install --upgrade pyinstaller pandas openpyxl pdfplumber pdfminer.six pillow PyPDF2 chardet

echo.
echo =============================
echo 4) Checando icone
echo =============================
set ICON_SWITCH=
if exist "icone_jhervilha.ico" (
    set ICON_SWITCH=--icon=icone_jhervilha.ico
) else (
    echo [Atenção] arquivo icone_jhervilha.ico nao encontrado. O exe sera gerado sem icone.
)

echo.
echo =============================
echo 5) Gerando EXE com PyInstaller
echo =============================
pyinstaller --noconfirm --onefile ^
    %ICON_SWITCH% ^
    --name "JHervilha_Contas" ^
    --hidden-import=pdfplumber ^
    --hidden-import=pdfminer.high_level ^
    --hidden-import=pandas ^
    JHervilha_Contas.py

if errorlevel 1 (
    echo [ERRO] PyInstaller retornou erro. Verifique mensagens acima.
    pause
    exit /b 1
)

echo.
echo =============================
echo 6) Montando pacote final em dist\JHervilha-Contas
echo =============================
set PKG=dist\JHervilha-Contas
mkdir "%PKG%" 2>nul
mkdir "%PKG%\FATURAS" 2>nul
mkdir "%PKG%\BACKUP" 2>nul
mkdir "%PKG%\LOGS" 2>nul
mkdir "%PKG%\DEBUG" 2>nul

REM copia o exe gerado para a pasta do pacote
if exist "dist\JHervilha_Contas.exe" (
    move /y "dist\JHervilha_Contas.exe" "%PKG%\" >nul
) else (
    echo [AVISO] exe nao encontrado em dist\ (verifique o build).
)

REM copia a planilha inicial (se houver)
if exist "Controle Financeiro - JHervilha.xlsx" (
    copy /y "Controle Financeiro - JHervilha.xlsx" "%PKG%\" >nul
)

REM cria README simples na pasta do pacote
(
echo JHervilha - Contas
echo ===================
echo Como usar:
echo 1) Coloque as faturas (PDFs) na pasta FATURAS.
echo 2) Dê duplo clique em JHervilha_Contas.exe.
echo 3) Ao finalizar, verifique:
echo    - Controle Financeiro - JHervilha.xlsx (aba MM-YYYY)
echo    - Backups na pasta BACKUP
echo    - Logs na pasta LOGS
) > "%PKG%\README.txt"

echo.
echo [OK] Pacote criado em %PKG%
pause
endlocal
