#!/usr/bin/env bash
# Prepara o app para empacotar: copia ../assets para app/assets (o Buildozer só enxerga a pasta do app)
# e baixa as 78 cartas Rider-Waite para que o APK funcione offline.
set -e
cd "$(dirname "$0")"
python3 baixar_cartas.py
rm -rf assets && cp -r ../assets ./assets
echo "Pronto. Agora rode: buildozer -v android debug"
