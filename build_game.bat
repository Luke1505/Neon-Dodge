@echo off
echo Building NeonDodge.exe with PyInstaller...
pyinstaller --onefile --noconsole --add-data "assets;assets" --add-data "lang;lang" main.py --icon="assets/icon.ico" --name NeonDodge
echo Build process complete. Check the 'dist' folder for NeonDodge.exe
pause