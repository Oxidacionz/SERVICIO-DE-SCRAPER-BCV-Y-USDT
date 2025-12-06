import asyncio
from supabase import create_client, Client
from src.config import ProjectConfig
from datetime import datetime, timezone

# ID Fijo para actualizar siempre el mismo registro global
RAILWAY_RATES_ID = "00000000-0000-0000-0000-000000000001"

async def distribute_data(data: dict, projects: list[ProjectConfig]) -> dict:
    """
    Función principal de Fan-Out: Envía los datos actualizados a todas las bases de datos configuradas.
    """
    results = {}
    
    # 1. Preparar Payload (Schema de DB)
    # Mapeamos nuestro diccionario de dominio a las columnas de la tabla 'exchange_rates'
    # Nota: Asumimos 0.0 para BCV hasta que se implemente ese scraper.
    supabase_payload = {
        "id": RAILWAY_RATES_ID,
        "is_global": True,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        
        # Datos de Binance
        "usd_binance_buy": data.get("binance_p2p", {}).get("buy"),
        "usd_binance_sell": data.get("binance_p2p", {}).get("sell"),
        
        # Datos de BCV
        "usd_bcv": data.get("bcv", {}).get("usd", 0.0), 
        "eur_bcv": data.get("bcv", {}).get("eur", 0.0)
    }

    # 2. Crear Tareas Asíncronas (No bloqueantes)
    tasks = []
    for project in projects:
        tasks.append(_safe_update_project(project, supabase_payload))
    
    # 3. Ejecutar en paralelo (Concurrency)
    completed_results = await asyncio.gather(*tasks)
    
    # 4. Recopilar resultados
    for res in completed_results:
        results[res["project"]] = res["status"]
        
    return results

async def _safe_update_project(project: ProjectConfig, payload: dict) -> dict:
    """
    Intenta actualizar un solo proyecto controlando errores aislados (Bulkhead Pattern).
    """
    try:
        # Nota: Crear el cliente es ligero.
        supabase: Client = create_client(project.supabase_url, project.supabase_key)
        
        # Ejecutamos upsert
        # .upsert(payload) crea o actualiza basado en la PK 'id'
        response = supabase.table("exchange_rates").upsert(payload).execute()
        
        # Validamos respuesta básica (Supabase postgrest suele lanzar excepcion si falla, pero por si acaso)
        if not response.data:
            # A veces upsert retorna data vacía si no hay return values, pero execute() suele traerlo.
            # Asumimos éxito si no hubo throw.
            pass

        return {"project": project.name, "status": "success"}
        
    except Exception as e:
        # Logueamos el error pero no detenemos el loop principal
        print(f"❌ Fallo al actualizar DB de proyecto '{project.name}': {str(e)}")
        return {"project": project.name, "status": f"error: {str(e)}"}
