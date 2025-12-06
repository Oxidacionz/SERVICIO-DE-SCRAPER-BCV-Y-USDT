import os
import json
import asyncio
from main import main

# Configuración de prueba con las credenciales reales provistas
test_config = [
  {
    "name": "SB_FINANCIAL",
    "supabase_url": "https://zfesgvclmgzsaldjoyjq.supabase.co",
    "supabase_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmZXNndmNsbWd6c2FsZGpveWpxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDU2NzYzMywiZXhwIjoyMDgwMTQzNjMzfQ.MwVaRzId8hEltjV0jwoeQkRoDOsT_mxNvrLLffqumb0"
  },
  {
    "name": "TORO_GROUP",
    "supabase_url": "https://kkkwfimgkemxwgvqvaob.supabase.co",
    "supabase_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtra3dmaW1na2VteHdndnF2YW9iIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDM1MzYxNiwiZXhwIjoyMDc5OTI5NjE2fQ.knRIKPUcNkkJTrMJJO-gBUInYir-ALMQSlMDi_oByJc"
  }
]

# Inyectar en variable de entorno
os.environ["PROJECTS_CONFIG"] = json.dumps(test_config)

print("🧪 Iniciando Prueba de Integración Local...")
if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\n✅ Prueba finalizada. Verifica los logs arriba.")
    except Exception as e:
        print(f"\n❌ Falló la prueba: {e}")
