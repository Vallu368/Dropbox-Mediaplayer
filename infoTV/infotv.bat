@echo off
:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...
    :: Download the Python installer (64-bit)
    curl -o python_installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7.exe
    echo Running Python installer...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    echo Python installation complete. Please restart the script.
    pause
    exit /b
)

:: Define the path for the Startup folder and the path for the new batch file
set startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set new_bat_file=%startup_folder%\launcher.bat

:: Check if the new batch file already exists
if not exist "%new_bat_file%" (
    echo Creating new batch file to launch infotv.bat in Startup folder...
    (
        echo @echo off
        echo start "" "%~dp0infotv.bat"
    ) > "%new_bat_file%"
) else (
    echo The batch file to launch infotv.bat already exists in Startup folder.
)

:: Define the path for the scripts folder (assumed location relative to the batch file)
set scripts_folder=%~dp0scripts

:: If Python is installed, run install_requirements.py and mediaplayer.py
echo Python is already installed. Proceeding with installation of requirements...
python "%scripts_folder%\installation.py"

python "%scripts_folder%\refreshtoken.py"

echo Running Media Player...
python "%scripts_folder%\mediaplayer.py"

pause
