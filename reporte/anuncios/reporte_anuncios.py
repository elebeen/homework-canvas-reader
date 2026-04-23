from datetime import datetime, timedelta, timezone
from reporte.anuncios.get_announcements import get_course_announcements
from reporte.tareas.get_courses import get_canvas_courses 

def generate_announcements_report():
    cursos = get_canvas_courses()
    # Fecha de corte: hace 7 días (en hora local de Perú para comparar con tus objetos Announcement)
    hace_7_dias = (datetime.now(timezone.utc) - timedelta(hours=5)) - timedelta(days=7)
    
    reporte_anuncios = "📢 *ANUNCIOS DE LA ÚLTIMA SEMANA* 📢\n\n"
    hay_anuncios = False

    for curso in cursos:
        # Obtenemos los anuncios del curso
        todos_los_anuncios = get_course_announcements(curso.id)
        
        # Filtramos: que tengan fecha y que sea posterior a hace 7 días
        recientes = [
            a for a in todos_los_anuncios 
            if a.posted_at and a.posted_at >= hace_7_dias
        ]

        if recientes:
            hay_anuncios = True
            reporte_anuncios += f"🏛️ *{curso.name}*\n"
            for anunc in recientes:
                fecha_fmt = anunc.posted_at.strftime("%d/%m")
                reporte_anuncios += f"  • [{fecha_fmt}] {anunc.title}\n"
            reporte_anuncios += "\n"

    if not hay_anuncios:
        reporte_anuncios += "📭 No hay anuncios nuevos en los últimos 7 días."

    return reporte_anuncios