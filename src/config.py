import os
import json
from pydantic import BaseModel
from typing import List

class ProjectConfig(BaseModel):
    name: str
    supabase_url: str
    supabase_key: str

def load_projects() -> List[ProjectConfig]:
    """Carga configuración desde variable de entorno PROJECTS_CONFIG"""
    config_json = os.getenv("PROJECTS_CONFIG", "[]") # Espera un array de objetos JSON stringificado
    try:
        data = json.loads(config_json)
        return [ProjectConfig(**proj) for proj in data]
    except Exception as e:
        print(f"Error cargando configuracion de proyectos: {e}")
        return []
