import os
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from flask import Flask

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

# Instalar navegadores automáticamente
def install_browsers():
    from playwright.__main__ import main as playwright_install
    playwright_install()

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

# Lógica principal del bot
def run_bot_logic():
    global response_count
    with sync_playwright() as p:
        # Iniciar el navegador en modo headless
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Abrir WhatsApp Web
        page.goto("https://web.whatsapp.com")
        print("Esperando que se escanee el código QR...")
        try:
            # Esperar a que el QR sea escaneado
            page.wait_for_selector("canvas", timeout=60000)  # Espera 60 segundos
            print("Sesión iniciada correctamente.")
        except Exception:
            print("Error: No se detectó el código QR a tiempo.")
            browser.close()
            return

        # Buscar el grupo
        target_group = os.getenv("TARGET_GROUP", "App de inglés")
        try:
            search_box = page.wait_for_selector("div[role='textbox']", timeout=30000)
            search_box.fill(target_group)
            search_box.press("Enter")
            print(f"Grupo '{target_group}' seleccionado.")
        except Exception:
            print("Error: No se pudo encontrar el grupo.")
            browser.close()
            return

        # Enviar un mensaje inicial
        try:
            input_box = page.wait_for_selector("footer div[contenteditable='true']", timeout=30000)
            initial_message = get_time_based_response()
            input_box.fill(initial_message)
            input_box.press("Enter")
            print(f"Mensaje inicial enviado: {initial_message}")
        except Exception:
            print("Error: No se pudo enviar el mensaje inicial.")
            browser.close()
            return

        # Escucha activa para responder mensajes
        while response_count < max_responses:
            try:
                # Obtener los últimos mensajes
                messages = page.query_selector_all("span.selectable-text")
                if messages:
                    last_message = messages[-1].inner_text().lower()

                    for expected, reply in expected_messages.items():
                        if expected in last_message:
                            input_box = page.query_selector("footer div[contenteditable='true']")
                            input_box.fill(reply)
                            input_box.press("Enter")
                            print(f"Respondido con: {reply}")
                            response_count += 1
                            time.sleep(2)  # Evitar respuestas rápidas consecutivas
                            break
            except Exception as e:
                print(f"Error detectado en la escucha activa: {e}")
                time.sleep(5)

        browser.close()
        print("Bot detenido.")

# Flask para el servicio web
app = Flask(__name__)

@app.route("/")
def run_web_service():
    # Ejecutar la lógica del bot
    run_bot_logic()
    return "Bot ejecutándose correctamente."

if __name__ == "__main__":
    install_browsers()  # Instalar navegadores si no están presentes
    app.run(host="0.0.0.0", port=8080)
