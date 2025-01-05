import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar opciones de Chrome
chrome_options = Options()
# Comentado para que la interfaz gráfica esté habilitada
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Inicializar WebDriver
try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print(f"Error al inicializar WebDriver: {e}")
    exit(1)

# Respuestas dinámicas según el horario
morning_responses = [
    "¡Buenos días! ¿Cómo están todos?",
    "Espero que tengan un excelente inicio de día.",
    "¡Buenos días, grupo!"
]

afternoon_responses = [
    "¡Buenas tardes! ¿Cómo les va?",
    "Espero que estén disfrutando de su tarde.",
    "¡Buenas tardes a todos!"
]

night_responses = [
    "¡Buenas noches! Que descansen.",
    "Espero que hayan tenido un gran día. ¡Buenas noches!",
    "¡Buenas noches, grupo!"
]

# Banco de respuestas esperadas y respuestas automáticas
expected_messages = {
    "hola": "¡Hola! ¿Cómo estás?",
    "¿cómo estás?": "¡Estoy bien! ¿Y tú?",
    "gracias": "¡De nada! ¿En qué más te puedo ayudar?",
    "buenas tardes": "¡Buenas tardes! Espero que estés teniendo un excelente día.",
    "adiós": "¡Hasta luego! Cuídate."
}

# Limitar el número de respuestas
max_responses = 5
response_count = 0

# Función para obtener respuesta dinámica según la hora
def get_time_based_response():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return random.choice(morning_responses)
    elif 12 <= current_hour < 18:
        return random.choice(afternoon_responses)
    elif 18 <= current_hour < 23:
        return random.choice(night_responses)
    else:
        return "¡Hola! ¿Cómo están todos?"

# Función para capturar el estado de la página
def take_screenshot(driver, name):
    driver.save_screenshot(f"{name}.png")

# Inicializar el bot
try:
    # Código para iniciar el navegador y escanear el código QR
    print("Iniciando el navegador...")
    driver.get("https://web.whatsapp.com")

    print("Esperando que se escanee el código QR...")
    try:
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas")))
        take_screenshot(driver, "qr_detected")
        print("Sesión iniciada correctamente.")
    except Exception as e:
        take_screenshot(driver, "qr_not_detected")
        print("Error: No se detectó el código QR a tiempo. Verifica que WhatsApp Web haya cargado correctamente.")
        driver.quit()
        exit(1)

    # Obtener el nombre del grupo desde variables de entorno
    target_group = os.getenv("TARGET_GROUP", "App de inglés")

    # Seleccionar el grupo o contacto
    try:
        search_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
        )
        search_box.click()
        search_box.send_keys(target_group)
        search_box.send_keys(Keys.ENTER)
        take_screenshot(driver, "group_selected")
        print(f"Grupo '{target_group}' seleccionado.")

        # Enviar un mensaje inicial basado en la hora del día
        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "footer div[contenteditable='true']"))
        )
        initial_message = get_time_based_response()
        input_box.click()
        input_box.send_keys(initial_message)
        input_box.send_keys(Keys.ENTER)
        print(f"Mensaje inicial enviado: {initial_message}")
    except Exception as e:
        take_screenshot(driver, "search_box_error")
        print(f"Error: No se pudo encontrar el cuadro de búsqueda o enviar el mensaje inicial. Asegúrate de que el nombre del grupo '{target_group}' sea correcto y que esté disponible en WhatsApp Web.")
        driver.quit()
        exit(1)

    # Escucha activa para responder mensajes
    while True:
        try:
            if response_count >= max_responses:
                print("Se ha alcanzado el límite de respuestas permitidas.")
                break

            messages = driver.find_elements(By.CSS_SELECTOR, "span.selectable-text")
            if messages:
                last_message = messages[-1].text.lower()

                for expected, reply in expected_messages.items():
                    if expected in last_message:
                        input_box = driver.find_element(By.CSS_SELECTOR, "footer div[contenteditable='true']")
                        input_box.click()
                        input_box.send_keys(reply)
                        input_box.send_keys(Keys.ENTER)
                        print(f"Respondido con: {reply}")
                        response_count += 1
                        time.sleep(2)  # Evitar respuestas rápidas consecutivas
                        break

            time.sleep(5)
        except Exception as e:
            take_screenshot(driver, "error_in_loop")
            print(f"Error detectado en la escucha activa: {e}")
            time.sleep(5)
except KeyboardInterrupt:
    print("Bot detenido manualmente.")
except Exception as e:
    take_screenshot(driver, "general_error")
    print(f"Error al iniciar el bot: {e}")
finally:
    driver.quit()
    print("Navegador cerrado.")
