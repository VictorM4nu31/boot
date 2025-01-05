#!/usr/bin/env bash

# Instalar Chrome y chromedriver
echo "Instalando Google Chrome y ChromeDriver..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Instalar ChromeDriver
CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9.]{2,}' | head -1)
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*})
wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
sudo mv chromedriver /usr/local/bin/

echo "Instalando dependencias de Python..."
pip install -r requirements.txt
