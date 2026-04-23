import requests
from datetime import datetime, timedelta
from config import Config
from modelos.canva_models import Announcement

def get_course_announcements(course_id: int):
    Config.validate()

    url = f"{Config.BASE_URL}/courses/{course_id}/discussion_topics"
    params = {
        "only_announcements": "true",
        "per_page": 5 # Probablemente solo quieras los últimos anuncios
    }
    
    try:
        response = requests.get(url, headers=Config.HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        
        announcements = []
        for item in data:
            # Convertimos las fechas y ajustamos a hora de Perú (-5h)
            raw_date = item.get("posted_at")
            posted_at_peru = None
            if raw_date:
                utc_date = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                posted_at_peru = utc_date - timedelta(hours=5)

            announcement = Announcement(
                id=item["id"],
                title=item["title"],
                message=item.get("message", ""),
                posted_at=posted_at_peru,
                author_name=item.get("author", {}).get("display_name", "Profesor"),
                url=item["html_url"]
            )
            announcements.append(announcement)
            
        return announcements
    except Exception as e:
        print(f"Error obteniendo anuncios del curso {course_id}: {e}")
        return []