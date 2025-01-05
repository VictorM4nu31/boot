#!/usr/bin/env bash

# Instalar dependencias del sistema necesarias para Playwright
echo "Instalando dependencias del sistema necesarias para Playwright..."
apt-get update
apt-get install -y libnss3 libatk-bridge2.0-0 libxcomposite1 libxrandr2 \
libgbm1 libpangocairo-1.0-0 libasound2 libxdamage1 libxkbcommon0 libgtk-3-0 \
libdrm2 libxshmfence1 libegl1 libenchant-2-2 libsecret-1-0 libmanette-0.2-0 \
libavif15 libgstcodecparsers-1.0-0 libgstgl-1.0-0 libgles2

# Instalar navegadores de Playwright
echo "Instalando navegadores de Playwright..."
npx playwright install
