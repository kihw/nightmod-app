@echo off
REM Script d'installation pour NightMod (Windows)

echo Installation de NightMod...

REM Vérifier si Python est installé
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python avant de continuer.
    pause
    exit /b 1
)

REM Créer répertoire de destination
set INSTALL_DIR=%LOCALAPPDATA%\NightMod
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\assets" mkdir "%INSTALL_DIR%\assets"

REM Copier les fichiers
echo Copie des fichiers...
copy /Y nightmod.py "%INSTALL_DIR%\" > nul
if exist assets xcopy /Y /E assets\* "%INSTALL_DIR%\assets\" > nul
if exist requirements.txt copy /Y requirements.txt "%INSTALL_DIR%\" > nul

REM Installer les dépendances
echo Installation des dependances...
pip install -r requirements.txt

REM Créer un raccourci sur le bureau
echo Création du raccourci...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\NightMod.lnk'); $Shortcut.TargetPath = 'pythonw.exe'; $Shortcut.Arguments = '%INSTALL_DIR%\nightmod.py'; $Shortcut.IconLocation = '%INSTALL_DIR%\assets\icon.ico,0'; $Shortcut.Save()"

REM Créer un raccourci dans le menu Démarrer
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\NightMod" mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\NightMod"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\NightMod\NightMod.lnk'); $Shortcut.TargetPath = 'pythonw.exe'; $Shortcut.Arguments = '%INSTALL_DIR%\nightmod.py'; $Shortcut.IconLocation = '%INSTALL_DIR%\assets\icon.ico,0'; $Shortcut.Save()"

echo Installation terminee!
echo Vous pouvez lancer NightMod depuis le raccourci sur votre bureau ou depuis le menu Demarrer.
pause