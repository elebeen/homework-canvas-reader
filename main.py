from reporte.tareas.reporte_tareas import generate_global_report
from reporte.anuncios.reporte_anuncios import generate_announcements_report

# Ejecución
if __name__ == "__main__":
    tareas = generate_global_report()
    print(tareas)

    anuncios = generate_announcements_report()
    print(anuncios)