import asyncio
from src.config import load_projects
from datetime import datetime

async def main():
    print(f"🚀 Iniciando Scraper Service - {datetime.now()}")
    
    projects = load_projects()
    print(f"📋 Proyectos configurados: {len(projects)}")
    
    if not projects:
        print("⚠️ Advertencia: No se encontraron proyectos en la variable de entorno PROJECTS_CONFIG.")
        print("ℹ️ Asegúrate de configurarla en Railway o en tu .env local como un array JSON válido.")
        
    print("⏳ (Fase 1 completada. Lógica de scraping pendiente para Fase 2)")

if __name__ == "__main__":
    asyncio.run(main())
