#!/bin/bash
echo "========================================"
echo " MEMBUAT FISCH AUTO APPRAISER"
echo "========================================"
echo ""
echo "Membersihkan build sebelumnya..."
rm -rf build dist
echo ""
echo "Mengkompilasi aplikasi..."
pyinstaller --onefile --windowed --name="FischAppraiser" --add-data "appraiser_config.json:." main.py
echo ""
echo "========================================"
echo " SELESAI! Cek folder 'dist'"
echo "========================================"