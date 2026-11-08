"""
Cerbero - Perfiles de objetivo (headless).

Carga un perfil desde YAML o JSON y lo convierte al diccionario `info`
interno que consumen los motores, de modo que el modo no interactivo
produzca exactamente lo mismo que el cuestionario interactivo.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from .utils import normalize_string


class ProfileError(Exception):
    """Error al cargar o validar un perfil de objetivo."""


_DATE_FORMATS = ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d")


def parse_date(value: Any) -> Optional[datetime]:
    """Convierte una fecha (date, datetime o string) en datetime, o None."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, str):
        for fmt in _DATE_FORMATS:
            try:
                return datetime.strptime(value.strip(), fmt)
            except ValueError:
                continue
        raise ProfileError(
            f"Fecha no reconocida: {value!r}. Usa DD/MM/YYYY o YYYY-MM-DD."
        )
    raise ProfileError(f"Tipo de fecha no soportado: {type(value).__name__}")


def _as_word_list(value: Any) -> List[str]:
    """Normaliza un campo que puede ser string o lista en lista de palabras."""
    if value is None:
        return []
    if isinstance(value, str):
        items = value.replace(",", " ").split()
    elif isinstance(value, list):
        items = [str(v) for v in value]
    else:
        raise ProfileError(f"Se esperaba texto o lista, se recibió {type(value).__name__}")
    out: List[str] = []
    for item in items:
        cleaned = normalize_string(str(item))
        if cleaned:
            out.append(cleaned)
    return out


def _as_str_list(value: Any) -> List[str]:
    """Lista de strings tal cual (para frases/números), separando por coma."""
    if value is None:
        return []
    if isinstance(value, str):
        parts = [p.strip() for p in value.split(",")]
    elif isinstance(value, list):
        parts = [str(v).strip() for v in value]
    else:
        raise ProfileError(f"Se esperaba texto o lista, se recibió {type(value).__name__}")
    return [p for p in parts if p]


def build_info(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construye el diccionario `info` interno desde un dict crudo (YAML/JSON).

    Acepta claves `persona_principal`/`principal`, `pareja`, `hijos`, `otros`.
    """
    if not isinstance(raw, dict):
        raise ProfileError("El perfil debe ser un mapa (clave: valor) en su raíz.")

    principal_raw = raw.get("persona_principal") or raw.get("principal") or {}
    pareja_raw = raw.get("pareja") or (raw.get("familia", {}) or {}).get("pareja") or {}
    hijos_raw = raw.get("hijos") or (raw.get("familia", {}) or {}).get("hijos") or []
    otros_raw = raw.get("otros") or raw.get("otros_datos") or {}

    if not isinstance(hijos_raw, list):
        raise ProfileError("'hijos' debe ser una lista.")

    info: Dict[str, Any] = {
        "persona_principal": {
            "nombres": _as_word_list(principal_raw.get("nombres")),
            "apellidos": _as_word_list(principal_raw.get("apellidos")),
            "fecha_nacimiento": parse_date(principal_raw.get("fecha_nacimiento")),
            "sobrenombre": (normalize_string(str(principal_raw.get("sobrenombre", "")))),
        },
        "familia": {
            "pareja": {
                "nombres": _as_word_list(pareja_raw.get("nombres")),
                "apellidos": _as_word_list(pareja_raw.get("apellidos")),
                "fecha_nacimiento": parse_date(pareja_raw.get("fecha_nacimiento")),
            },
            "hijos": [
                {
                    "nombres": _as_word_list(h.get("nombres")),
                    "apellidos": _as_word_list(h.get("apellidos")),
                    "fecha_nacimiento": parse_date(h.get("fecha_nacimiento")),
                }
                for h in hijos_raw
            ],
        },
        "otros_datos": {
            "mascota": normalize_string(str(otros_raw.get("mascota", ""))),
            "frases": _as_word_list(otros_raw.get("frases")),
            "numeros_importantes": _as_str_list(otros_raw.get("numeros_importantes")),
            "mangle_phrases": _as_str_list(otros_raw.get("mangle_phrases")),
        },
    }

    pp = info["persona_principal"]
    if not pp["nombres"] and not pp["apellidos"] and not info["otros_datos"]["frases"]:
        raise ProfileError(
            "El perfil no contiene datos utilizables (ni nombres, ni apellidos, ni frases)."
        )
    return info


def load_profile(path: str) -> Dict[str, Any]:
    """Carga un perfil desde un archivo .yaml/.yml/.json y devuelve `info`."""
    if not os.path.exists(path):
        raise ProfileError(f"No se encontró el archivo de perfil: {path}")

    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    raw: Any
    if path.lower().endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise ProfileError(
                "Falta PyYAML para leer perfiles YAML. Instala con: pip install pyyaml"
            ) from exc
        raw = yaml.safe_load(content)
    elif path.lower().endswith(".json"):
        raw = json.loads(content)
    else:
        # Intentar YAML primero (superset de JSON), luego JSON.
        try:
            import yaml

            raw = yaml.safe_load(content)
        except Exception:
            raw = json.loads(content)

    if raw is None:
        raise ProfileError("El perfil está vacío.")
    return build_info(raw)


EXAMPLE_PROFILE_YAML = """\
# Perfil de objetivo para Cerbero (headless)
# Uso:  cerbero generate --config perfil.yaml --engines all --output wl.txt
# Deja en blanco u omite lo que no apliques. Las fechas aceptan
# DD/MM/YYYY o YYYY-MM-DD.

persona_principal:
  nombres: [José, Luis]
  apellidos: [Núñez, Rojas]
  fecha_nacimiento: 1985-07-12
  sobrenombre: Pepe

pareja:
  nombres: [María]
  apellidos: [Soto]
  fecha_nacimiento: 02/03/1987

hijos:
  - nombres: [Benjamín]
    apellidos: [Núñez, Soto]
    fecha_nacimiento: 2012-09-01
  - nombres: [Sofía]
    fecha_nacimiento: 2015-05-20

otros:
  mascota: Firulais
  frases: [Red Segura, Mi Empresa]
  numeros_importantes: ["1234", "742"]
  mangle_phrases: [Red Segura]
"""
