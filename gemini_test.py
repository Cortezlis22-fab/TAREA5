
import os
from dotenv import load_dotenv
from google import genai

print("1. Iniciando prueba...")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: No se encontro la API key.")
    raise SystemExit

print("2. API key encontrada.")

try:
    client = genai.Client(api_key=api_key)
    print("3. Cliente de Gemini creado.")
    
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Hola Gemini. Responde: conexion exitosa."
    )

    print("4. Respuesta recibida:")
    print(response.text)

    client.close()

except Exception as error:
    print("ERROR AL CONECTAR CON GEMINI:")
    print(type(error).__name__)
    print(error)
