import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# Instalar automáticamente el ChromeDriver compatible
chromedriver_autoinstaller.install()

# Configurar el ejecutable de Chrome
CHROME_BINARY_PATH = "/usr/bin/google-chrome"  # Ruta del binario de Chrome en Render

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Modo sin interfaz gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = CHROME_BINARY_PATH

# Configurar servicio de ChromeDriver
service = Service()

# Inicializar WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Respuestas dinámicas según el horario
morning_responses = ["¡Buenos días!", "¿Listos para otro día?", "¡Hola! Que tengan un buen día."]
afternoon_responses = ["¡Buenas tardes! ¿Cómo va todo?", "Hola, ¿qué tal su día?"]
night_responses = ["¡Buenas noches! Que descansen.", "Buenas noches, ¿cómo estuvo su día?"]
general_responses = ["¡Hola! ¿Qué tal?", "¡Buenas! ¿Cómo están?"]

def get_time_based_response():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return random.choice(morning_responses)
    elif 12 <= current_hour < 18:
        return random.choice(afternoon_responses)
    elif 18 <= current_hour < 23:
        return random.choice(night_responses)
    else:
        return random.choice(general_responses)

# Inicializar el bot
try:
    print("Iniciando el navegador...")
    driver.get("https://web.whatsapp.com")

    print("Esperando que se escanee el código QR...")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._3Ul489")))
    print("Sesión iniciada correctamente.")

    # Obtener el nombre del grupo desde variables de entorno
    target_group = os.getenv("TARGET_GROUP", "NombrePorDefecto")

    # Seleccionar el grupo o contacto
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "._3FRCZ.copyable-text.selectable-text"))
    )
    search_box.click()
    search_box.send_keys(target_group)
    search_box.send_keys(Keys.ENTER)

    print(f"Grupo '{target_group}' seleccionado.")

    # Escucha activa para responder mensajes
    while True:
        try:
            messages = driver.find_elements(By.CSS_SELECTOR, "._1Gy50")
            if messages:
                last_message = messages[-1].text.lower()

                if any(greeting in last_message for greeting in ["hola", "buenos días", "buenas tardes", "buenas noches"]):
                    response = get_time_based_response()
                    input_box = driver.find_element(By.CSS_SELECTOR, "._3FRCZ.copyable-text.selectable-text")
                    input_box.click()
                    input_box.send_keys(response)
                    input_box.send_keys(Keys.ENTER)
                    print(f"Respondido con: {response}")

            time.sleep(5)
        except Exception as e:
            print(f"Error detectado: {e}")
            time.sleep(5)
except KeyboardInterrupt:
    print("Bot detenido manualmente.")
except Exception as e:
    print(f"Error al iniciar el bot: {e}")
finally:
    driver.quit()
    print("Navegador cerrado.")
