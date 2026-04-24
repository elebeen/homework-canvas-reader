from reporte.tareas.reporte_tareas import generate_global_report
from reporte.anuncios.reporte_anuncios import generate_announcements_report
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_to_whatsapp_api(report_text):
    url = "http://localhost:3000/send-report"
    payload = {
        "message": report_text,
        "number": os.getenv("NUMBER")
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ ¡Reporte entregado a la API de WhatsApp!")
        else:
            print(f"⚠️ Error en la API: {response.text}")
    except Exception as e:
        print(f"❌ No se pudo conectar con el servidor Express: {e}")

# Ejecución
if __name__ == "__main__":
    reporte = generate_global_report()
    send_to_whatsapp_api(reporte)

    # anuncios = generate_announcements_report()
    # print(anuncios)

    # tareas = generate_global_report()
    # print(tareas)