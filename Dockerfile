# Usa una imagen base con soporte para Python
FROM python:3.11-slim

# Instala las dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libxcomposite1 libxrandr2 \
    libgbm1 libpangocairo-1.0-0 libasound2 libxdamage1 libxkbcommon0 libgtk-3-0 \
    libdrm2 libxshmfence1 libegl1 libenchant-2-2 libsecret-1-0 libmanette-0.2-0 \
    libavif15 libgstcodecparsers-1.0-0 libgstgl-1.0-0 libgles2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala navegadores de Playwright
RUN npx playwright install

# Define el comando de inicio
CMD ["python", "boot.py"]
