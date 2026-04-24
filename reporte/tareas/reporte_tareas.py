from reporte.tareas.get_courses import get_canvas_courses
from reporte.tareas.get_assigments import get_assignments_with_submission_status
from datetime import datetime, timezone, timedelta
from datetime import date


# def generate_global_report():
#     cursos = get_canvas_courses() 
#     ahora = datetime.now(timezone.utc)
#     ahora_peru = ahora - timedelta(hours=5)
    
#     reporte_final = "*REPORTE DE TAREAS PENDIENTES*\n\n"
#     # Diccionario para agrupar tareas sin fecha por curso
#     # { "Nombre del Curso": [lista_de_tareas] }
#     sin_fecha_por_curso = {}
#     hay_tareas_con_fecha = False

#     for curso in cursos:
#         tareas = get_assignments_with_submission_status(curso.id) 
        
#         # Filtramos primero lo pendiente y futuro
#         pendientes = [
#             t for t in tareas 
#             if t.submission.workflow_state == 'unsubmitted' and 
#             (not t.end_at or datetime.fromisoformat(t.end_at.replace("Z", "+00:00")) > ahora)
#         ]

#         # Separamos las que tienen fecha de las que no
#         con_fecha = [t for t in pendientes if t.end_at is not None]
#         sin_fecha = [t for t in pendientes if t.end_at is None]

#         # 1. Procesamos tareas CON fecha (se muestran bajo el nombre del curso)
#         if con_fecha:
#             hay_tareas_con_fecha = True
#             reporte_final += f" *{curso.name}*\n"
#             for p in con_fecha:
#                 fecha_peru = datetime.fromisoformat(p.end_at.replace("Z", "+00:00")) - timedelta(hours=5)
                
#                 if fecha_peru.date() == ahora_peru.date():
#                     fecha_txt = f"Hoy a las {fecha_peru.strftime('%H:%M')}"
#                 elif fecha_peru.date() == (ahora_peru + timedelta(days=1)).date():
#                     fecha_txt = f"Mañana a las {fecha_peru.strftime('%H:%M')}"
#                 else:
#                     fecha_txt = fecha_peru.strftime("%d/%m %H:%M")
                
#                 reporte_final += f"""  • {p.title}\n     Vence: {fecha_txt}\nlink {p.html_url}\n"""
#             reporte_final += "\n"

#         # 2. Guardamos las tareas SIN fecha para el final
#         if sin_fecha:
#             sin_fecha_por_curso[curso.name] = sin_fecha

#     # 3. Sección especial para tareas sin fecha
#     if sin_fecha_por_curso:
#         reporte_final += "---" * 5 + "\n"
#         reporte_final += "*TAREAS SIN FECHA ESTABLECIDA*\n"
#         for curso_nombre, tareas_list in sin_fecha_por_curso.items():
#             reporte_final += f"*{curso_nombre}*:\n"
#             for s in tareas_list:
#                 reporte_final += f"  • {s.title}\n"
#             reporte_final += "\n"

#     if not hay_tareas_con_fecha and not sin_fecha_por_curso:
#         reporte_final += "¡Todo al día! No hay tareas pendientes."

#     return reporte_final

from collections import defaultdict
from datetime import datetime, timezone, timedelta

def generate_global_report():
    cursos = get_canvas_courses()
    ahora = datetime.now(timezone.utc)
    ahora_peru = ahora - timedelta(hours=5)
    
    # Estructura para agrupar: { fecha_date_obj: [lista_de_tareas_con_curso] }
    tasks_by_date = defaultdict(list)
    tasks_no_date = []

    # 1. Recolectar todas las tareas de todos los cursos
    for curso in cursos:
        tareas = get_assignments_with_submission_status(curso.id)
        
        for t in tareas:
            # Filtro: debe ser 'unsubmitted' y tener fecha futura (o sin fecha)
            es_pendiente = t.submission.workflow_state == 'unsubmitted'
            es_futura = (not t.end_at or datetime.fromisoformat(t.end_at.replace("Z", "+00:00")) > ahora)
            
            if es_pendiente and es_futura:
                if t.end_at:
                    fecha_utc = datetime.fromisoformat(t.end_at.replace("Z", "+00:00"))
                    fecha_peru = fecha_utc - timedelta(hours=5)
                    tasks_by_date[fecha_peru.date()].append({'task': t, 'curso': curso.name.split(sep="-")[0], 'fecha_obj': fecha_peru})
                else:
                    tasks_no_date.append({'task': t, 'curso': curso.name})

    # 2. Ordenar las fechas
    sorted_dates = sorted(tasks_by_date.keys())
    
    # 3. Construir el reporte
    reporte_final = "*REPORTE DE TAREAS PENDIENTES*\n\n"
    
    # Mapeo de días para traducir (opcional pero recomendado)
    dias_es = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}

    for fecha in sorted_dates:
        # Título del día

        dia_nombre = dias_es.get(fecha.weekday(), "Día desconocido")
        reporte_final += f"{dia_nombre} {fecha.strftime('%d/%m')}\n"
        
        # Tareas de ese día
        for item in tasks_by_date[fecha]:
            t = item['task']
            curso_nombre = item['curso']
            hora = item['fecha_obj'].strftime('%H:%M')
            
            reporte_final += f"*{curso_nombre}*\n"
            reporte_final += f"Hora: {hora}\n"
            reporte_final += f"Tarea: {t.title}\n"
            reporte_final += f"{t.html_url}\n\n"

    # 4. Sección "Sin Fecha" al final
    # if tasks_no_date:
    #     reporte_final += "---" * 5 + "\n"
    #     reporte_final += "❓ *TAREAS SIN FECHA ESTABLECIDA*\n"
    #     for item in tasks_no_date:
    #         reporte_final += f"*{item['curso']}* -  {item['task'].title}\n"

    if not sorted_dates and not tasks_no_date:
        reporte_final += "¡Todo al día! No hay tareas pendientes."

    return reporte_final