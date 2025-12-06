# 💰 Servicio Distribuido de Scraping Financiero (BCV & USDT)

Este microservicio es el núcleo de obtención de datos financieros para el ecosistema de aplicaciones fintech de la organización. Diseñado con una arquitectura de **Alta Disponibilidad** y **Escalabilidad Modular**, este servicio obtine tasas de cambio en tiempo real y las distribuye simultáneamente a múltiples bases de datos de proyectos independientes.

## 🚀 Características Principales

- **Arquitectura Fan-Out Idempotente**: Capacidad para actualizar N bases de datos simultáneamente sin duplicidad de registros.
- **Tolerancia a Fallos (Bulkhead Pattern)**: El fallo en la conexión de un proyecto no afecta la integridad de los datos de los demás.
- **Diseño Config-Driven**: Agregar nuevos proyectos clientes es tan simple como actualizar una variable de entorno JSON, sin tocar el código fuente.
- **Validación Estricta**: Uso de Pydantic para garantizar la integridad de los datos financieros antes de la persistencia.
- **Soporte Multi-Fuente**: Preparado para extraer datos de Binance P2P, BCV (Banco Central de Venezuela) y otras fuentes futuras.

## 🛠️ Stack Tecnológico

- **Lenguaje**: Python 3.10+
- **Orquestación**: Railway (Cron Job)
- **Base de Datos**: Supabase (PostgreSQL)
- **Librerías Clave**:
  - `requests`: Para peticiones HTTP eficientes.
  - `pydantic`: Para validación de modelos de datos.
  - `supabase`: Cliente oficial para interacción con PostgreSQL.

## 📦 Estructura del Proyecto

```bash
Scraper-Financial-Service/
├── src/
│   ├── adapters/       # Adaptadores de conexión a bases de datos (Fan-Out)
│   ├── core/           # Lógica de negocio y scraping puro
│   └── config.py       # Gestor de configuración dinámica
├── main.py             # Entrypoint del servicio (Orquestador)
└── requirements.txt    # Dependencias del proyecto
```

## 🔧 Configuración para Despliegue

Este servicio espera una variable de entorno crítica llamada `PROJECTS_CONFIG` con el siguiente formato JSON:

```json
[
  {
    "name": "SB_FINANCIAL",
    "supabase_url": "https://tu-proyecto-sb.supabase.co",
    "supabase_key": "tu-service-role-key"
  },
  {
    "name": "TORO_GRUPO",
    "supabase_url": "https://tu-proyecto-toro.supabase.co",
    "supabase_key": "tu-service-role-key"
  }
]
```

## 🤝 Contribución

Este es un componente crítico de infraestructura. Cualquier PR debe pasar por validación estricta de:
1.  Manejo de excepciones en red.
2.  Validación de tipos de datos.

---
**Desarrollado con ❤️ para máxima eficiencia financiera.**
