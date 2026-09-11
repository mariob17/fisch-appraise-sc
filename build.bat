@echo off
cd /d "%~dp0"
echo ========================================
echo  MEMBUAT FISCH AUTO APPRAISER .EXE
echo ========================================
echo.
echo Membersihkan build sebelumnya...
rmdir /s /q build dist 2>nul
echo.
echo Mengkompilasi aplikasi...
if exist "%~dp0venv\Scripts\python.exe" (
    "%~dp0venv\Scripts\python.exe" -m PyInstaller --onefile --windowed --name="FischAppraiser" --hidden-import rapidocr_onnxruntime --collect-submodules rapidocr_onnxruntime --add-data "appraiser_config.json;." --add-data "%~dp0venv\Lib\site-packages\rapidocr_onnxruntime\config.yaml;rapidocr_onnxruntime" --add-data "%~dp0venv\Lib\site-packages\rapidocr_onnxruntime\models;rapidocr_onnxruntime\models" main.py
) else (
    pyinstaller --onefile --windowed --name="FischAppraiser" --hidden-import rapidocr_onnxruntime --collect-submodules rapidocr_onnxruntime --add-data "appraiser_config.json;." --add-data "%~dp0venv\Lib\site-packages\rapidocr_onnxruntime\config.yaml;rapidocr_onnxruntime" --add-data "%~dp0venv\Lib\site-packages\rapidocr_onnxruntime\models;rapidocr_onnxruntime\models" main.py
)
echo.
echo ========================================
echo  SELESAI! Cek folder 'dist'
echo ========================================