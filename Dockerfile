# Usar una imagen base con Chrome y Selenium preinstalados
FROM selenium/standalone-chrome:4.12.0

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de tu proyecto al contenedor
COPY . .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Establecer el comando para ejecutar la aplicación
CMD ["python", "boot.py"]
