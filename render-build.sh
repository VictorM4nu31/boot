#!/usr/bin/env bash

# Instalar las dependencias del sistema necesarias para Playwright
echo "Instalando dependencias del sistema necesarias para Playwright..."
apt-get update
apt-get install -y libnss3 libatk-bridge2.0-0 libxcomposite1 libxrandr2 libgbm1 libpangocairo-1.0-0 libasound2 libxdamage1 libxkbcommon0 libgtk-3-0 libdrm2 libxshmfence1 libegl1

# Instalar navegadores de Playwright
echo "Instalando navegadores de Playwright..."
playwright install
