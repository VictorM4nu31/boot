import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración para Selenium en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--user-data-dir=/tmp/user_data")  # Carpeta temporal para sesión
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Frases de respuesta dinámica
morning_responses = [
    "¡Buenos días! 😊",
    "¿Qué tal? Espero que tengan un gran día.",
    "¡Hola! Listos para otro día.",
    "Buen día, gente bonita. ¿Cómo están?",
    "¡Hola! Que tengan un día increíble."
]

afternoon_responses = [
    "¡Buenas tardes! ¿Cómo va todo?",
    "Hola, buenas tardes. ¿Qué tal su día?",
    "¡Buenas tardes! Espero que estén teniendo un buen día.",
    "Que tal, buen día a todos.",
    "¡Buenas tardes! ¿Qué tal la jornada?"
]

night_responses = [
    "¡Buenas noches! Que descansen bien.",
    "Buenas noches. ¿Cómo estuvo su día?",
    "¡Buenas noches! Espero que haya sido un día genial.",
    "Buenas noches, grupo. No olviden descansar.",
    "¡Chicos, descansen! Mañana será otro gran día."
]

general_responses = [
    "¡Hola! ¿Cómo están todos?",
    "¡Buenas! ¿Qué tal su día?",
    "¡Hola! Espero que estén bien.",
    "¡Hey! ¿Cómo van las cosas?",
    "¡Hola, equipo! ¿Qué cuentan?"
]

# Función para seleccionar respuesta basada en la hora
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

    # Obtener el grupo desde la variable de entorno
    target_group = os.getenv("TARGET_GROUP", "NombrePorDefecto")

    # Seleccionar el grupo
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "._3FRCZ.copyable-text.selectable-text"))
    )
    search_box.click()
    search_box.send_keys(target_group)
    search_box.send_keys(Keys.ENTER)

    print(f"Grupo '{target_group}' seleccionado.")

    while True:
        try:
            # Obtener el último mensaje
            messages = driver.find_elements(By.CSS_SELECTOR, "._1Gy50")
            if messages:
                last_message = messages[-1].text.lower()

                # Responder si el mensaje es un saludo
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
