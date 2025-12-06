from dotenv import load_dotenv

# Cargar variables de entorno locales
load_dotenv()

import asyncio
from src.config import load_projects
from src.core.scraper_logic import fetch_financial_data
from src.adapters.supabase_adapter import distribute_data
from datetime import datetime

async def main():
    print(f"🚀 Iniciando Scraper Service - {datetime.now()}")
    
    # 1. Cargar Configuración
    projects = load_projects()
    print(f"📋 Proyectos configurados: {len(projects)}")
    
    if not projects:
        print("⚠️ Advertencia: No se encontraron proyectos en la variable de entorno PROJECTS_CONFIG.")
        return
        
    # 2. Obtener Datos
    try:
        financial_data = await fetch_financial_data()
        if not financial_data:
            print("❌ No se obtuvieron datos de ninguna fuente.")
            return
        print(f"💰 Datos obtenidos: {list(financial_data.keys())}")
    except Exception as e:
        print(f"❌ Error Fatal en Scraping: {e}")
        return

    # 3. Distribuir a Bases de Datos (Fan-Out)
    print(f"🔌 Iniciando distribución a {len(projects)} proyectos...")
    report = await distribute_data(financial_data, projects)
    
    print("🏁 Reporte de Distribución:")
    for proj, status in report.items():
        icon = "✅" if status == "success" else "❌"
        print(f"   {icon} {proj}: {status}")

if __name__ == "__main__":
    asyncio.run(main())
