
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la clave sin mostrarla
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API key encontrada correctamente.")
else:
    print("ERROR: No se encontró la API key.")
