from dataclasses import dataclass
from typing import List, Optional, Literal
from datetime import datetime

@dataclass
class Submission:
    workflow_state: Literal['unsubmitted', 'submitted', 'graded', 'pending_review', 'not_graded']
    submitted_at: Optional[str] = None
    # Puedes agregar más campos aquí según necesites

@dataclass
class CanvasAssignment:
    id: int
    title: str
    html_url: str
    context_name: str
    course_id: int
    submission: Submission
    end_at: Optional[str] = None
    type: Optional[Literal['assignment', 'quiz', 'discussion_topic', 'event']] = None

@dataclass
class CanvasCourse:
    id: int
    name: str

@dataclass
class CourseGroup:
    id: int
    name: str
    assignments: List[CanvasAssignment] # Solo tareas NO completadas

@dataclass
class Announcement:
    id: int
    title: str
    message: str
    posted_at: datetime
    author_name: str
    url: str
    # 'available_until' suele ser None en anuncios a menos que estén programados
    available_until: Optional[datetime] = None