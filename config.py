# config.py
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

class Config:
    CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
    BASE_URL = os.getenv("CANVAS_BASE_URL")
    CYCLE = os.getenv("ACADEMIC_CYCLE", "C24 6to")
    OFFSET = int(os.getenv("TIMEZONE_OFFSET", -5))
    
    # Headers globales para no repetirlos en cada función
    HEADERS = {
        "Authorization": f"Bearer {CANVAS_TOKEN}"
    }

    @classmethod
    def validate(cls):
        """Verifica que las variables esenciales existan."""
        if not cls.CANVAS_TOKEN:
            raise ValueError("❌ Error: CANVAS_TOKEN no encontrado en el archivo .env")