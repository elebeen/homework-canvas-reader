from reporte.tareas.get_courses import get_canvas_courses
from reporte.tareas.get_assigments import get_assignments_with_submission_status
from datetime import datetime, timezone, timedelta

def generate_global_report():
    cursos = get_canvas_courses() 
    ahora = datetime.now(timezone.utc)
    ahora_peru = ahora - timedelta(hours=5)
    
    reporte_final = "🚀 *REPORTE DE TAREAS PENDIENTES* 🚀\n\n"
    # Diccionario para agrupar tareas sin fecha por curso
    # { "Nombre del Curso": [lista_de_tareas] }
    sin_fecha_por_curso = {} 
    hay_tareas_con_fecha = False

    for curso in cursos:
        tareas = get_assignments_with_submission_status(curso.id) 
        
        # Filtramos primero lo pendiente y futuro
        pendientes = [
            t for t in tareas 
            if t.submission.workflow_state == 'unsubmitted' and 
            (not t.end_at or datetime.fromisoformat(t.end_at.replace("Z", "+00:00")) > ahora)
        ]

        # Separamos las que tienen fecha de las que no
        con_fecha = [t for t in pendientes if t.end_at is not None]
        sin_fecha = [t for t in pendientes if t.end_at is None]

        # 1. Procesamos tareas CON fecha (se muestran bajo el nombre del curso)
        if con_fecha:
            hay_tareas_con_fecha = True
            reporte_final += f"📘 *{curso.name}*\n"
            for p in con_fecha:
                fecha_peru = datetime.fromisoformat(p.end_at.replace("Z", "+00:00")) - timedelta(hours=5)
                
                if fecha_peru.date() == ahora_peru.date():
                    fecha_txt = f"Hoy a las {fecha_peru.strftime('%H:%M')}"
                elif fecha_peru.date() == (ahora_peru + timedelta(days=1)).date():
                    fecha_txt = f"Mañana a las {fecha_peru.strftime('%H:%M')}"
                else:
                    fecha_txt = fecha_peru.strftime("%d/%m %H:%M")
                
                reporte_final += f"""  • {p.title}\n    📅 Vence: {fecha_txt}\nlink {p.html_url}\n"""
            reporte_final += "\n"

        # 2. Guardamos las tareas SIN fecha para el final
        if sin_fecha:
            sin_fecha_por_curso[curso.name] = sin_fecha

    # 3. Sección especial para tareas sin fecha
    if sin_fecha_por_curso:
        reporte_final += "---" * 5 + "\n"
        reporte_final += "❓ *TAREAS SIN FECHA ESTABLECIDA*\n"
        for curso_nombre, tareas_list in sin_fecha_por_curso.items():
            reporte_final += f"*{curso_nombre}*:\n"
            for s in tareas_list:
                reporte_final += f"  • {s.title}\n"
            reporte_final += "\n"

    if not hay_tareas_con_fecha and not sin_fecha_por_curso:
        reporte_final += "✅ ¡Todo al día! No hay tareas pendientes."

    return reporte_final