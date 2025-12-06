# 🚀 Guía de Despliegue en Railway: Servicio de Scraping Distribuido

Sigue estos 4 pasos simplificados para activar tu microservicio en la nube.

---

### Paso 1: Conectar Repositorio
1. En tu Dashboard de Railway, haz clic en **New Project**.
2. Selecciona **Deploy from GitHub repo**.
3. Busca y selecciona: `Oxidacionz/SERVICIO-DE-SCRAPER-BCV-Y-USDT`.
4. Haz clic en **Deploy Now**.

---

### Paso 2: Configurar Variables de Entorno
El scraper necesita saber a qué bases de datos enviar la información.

1. Ve a la pestaña **Variables** de tu nuevo servicio.
2. Haz clic en **New Variable**.
3. **Variable Name:** `PROJECTS_CONFIG`
4. **Value:** (Copia y pega el siguiente bloque JSON completo):

```json
[
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
```
*(Nota: Estas son tus credenciales reales que ya validamos. Solo copia y pega).*

---

### Paso 3: Configurar Cron Job (Ejecución Periódica)
Queremos que el scraper corra cada 10 minutos automáticamente.

1. Ve a la pestaña **Settings**.
2. Baja hasta la sección **Cron Schedule**.
3. **Schedule:** Escribe `*/10 * * * *` (Esto significa "cada 10 minutos").
4. **Command:** Asegúrate que diga `python main.py`.

---

### Paso 4: Validar
1. Railway redesplegará automáticamente al guardar la variable o el Cron.
2. Ve a la pestaña **Deployments** y haz clic en el último deploy activo.
3. En la sección **Logs**, deberías ver algo así:

```text
🚀 Iniciando Scraper Service...
💰 Datos obtenidos: ['binance_p2p']
✅ SB_FINANCIAL: success
✅ TORO_GROUP: success
```

¡Listo! Tu arquitectura fintech ahora es modular y escalable. 🌍
