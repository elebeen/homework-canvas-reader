import requests
from typing import List
from config import Config
from modelos.canva_models import CanvasAssignment, Submission

def get_assignments_with_submission_status(course_id: int) -> List[CanvasAssignment]:
    Config.validate()
    
    """Réplica de getAssignmentsWithSubmissionStatus (Tareas por curso con estado)"""
    # Filtramos por bucket=upcoming para traer lo pendiente
    url = f"{Config.BASE_URL}/courses/{course_id}/assignments"
    params = {
        "include[]": "submission",
        "per_page": 100,
        "bucket": "unsubmitted"
    }

    try:
        response = requests.get(url, headers=Config.HEADERS, params=params)
        if response.status_code != 200:
            return []

        data = response.json()
        valid_assignments = []

        for item in data:
            # Filtramos solo los que tienen submission (equivalente al .filter de TS)
            sub = item.get("submission")
            if sub and sub.get("workflow_state"):
                # Mapeamos el JSON a nuestro objeto CanvasAssignment
                assignment = CanvasAssignment(
                    id=item["id"],
                    title=item["name"], # En la API el campo es 'name'
                    html_url=item["html_url"],
                    context_name="", # Se llena luego si es necesario
                    course_id=course_id,
                    end_at=item.get("due_at"), # Mapeamos due_at a end_at
                    type=item.get("type", "assignment"),
                    submission=Submission(
                        workflow_state=sub["workflow_state"],
                        submitted_at=sub.get("submitted_at")
                    )
                )
                valid_assignments.append(assignment)
        
        return valid_assignments
    except Exception as e:
        print(f"Error en curso {course_id}: {e}")
        return []