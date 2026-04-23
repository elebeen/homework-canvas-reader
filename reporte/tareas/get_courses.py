import requests
from config import Config
from modelos.canva_models import CanvasCourse

def get_canvas_courses():
    Config.validate()

    params = {
        "enrollment_state": "active",
        "per_page": 100
    }

    try:
        response = requests.get(f"{Config.BASE_URL}/courses", headers=Config.HEADERS, params=params)
        response.raise_for_status() # Lanza un error si la API responde algo mal (4xx o 5xx)
        
        data = response.json()

        # Filtramos y convertimos a objetos de la clase CanvasCourse
        objetos_cursos = [
            CanvasCourse(id=c["id"], name=c["name"]) 
            for c in data 
            if "name" in c and c["name"] and "C24 6to" in c["name"]
        ]
        
        return objetos_cursos

    except Exception as e:
        print(f"Error al obtener cursos: {e}")
        return []
