# coding: utf-8
"""
Cerbero v7.0 - Módulo de Entrada
Recopilación interactiva de información del usuario
"""

from __future__ import annotations
from datetime import datetime
from typing import Set, List, Dict
from core import Colors, safe_input, normalize_string


def gather_smart_information(required_sections: Set[str]) -> dict:
    """
    Recopila información personal de forma interactiva.

    Args:
        required_sections: Conjunto de secciones requeridas
                          ('principal', 'pareja', 'hijos', 'otros', 'mangle', 'familia')

    Returns:
        Diccionario con la información recopilada
    """
    print(f"{Colors.CYAN}--- Recopilación de Información Personal (deja en blanco si no aplica) ---{Colors.RESET}")
    info = {"persona_principal": {}, "familia": {"pareja": {}, "hijos": []}, "otros_datos": {}}

    if 'principal' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Datos del objetivo principal:")
        nombres_raw = safe_input("Nombres (ej: José): ", normalize=True)
        apellidos_raw = safe_input("Apellidos (ej: Núñez): ", normalize=True)
        info["persona_principal"]["nombres"] = [normalize_string(n) for n in nombres_raw.split()] if nombres_raw else []
        info["persona_principal"]["apellidos"] = [normalize_string(a) for a in apellidos_raw.split()] if apellidos_raw else []
        fecha = safe_input("Fecha de nacimiento (DD/MM/YYYY): ")
        try:
            info["persona_principal"]["fecha_nacimiento"] = datetime.strptime(fecha, "%d/%m/%Y") if fecha else None
        except ValueError:
            info["persona_principal"]["fecha_nacimiento"] = None
        info["persona_principal"]["sobrenombre"] = normalize_string(safe_input("Sobrenombre/Apodo: ", normalize=True))

    if 'pareja' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Datos de la Pareja:")
        nombres_p = safe_input("Nombres de la pareja: ", normalize=True)
        apellidos_p = safe_input("Apellidos de la pareja: ", normalize=True)
        info["familia"]["pareja"]["nombres"] = [normalize_string(n) for n in nombres_p.split()] if nombres_p else []
        info["familia"]["pareja"]["apellidos"] = [normalize_string(a) for a in apellidos_p.split()] if apellidos_p else []
        fecha_p = safe_input("Fecha de nacimiento de la pareja (DD/MM/YYYY): ")
        try:
            info["familia"]["pareja"]["fecha_nacimiento"] = datetime.strptime(fecha_p, "%d/%m/%Y") if fecha_p else None
        except ValueError:
            info["familia"]["pareja"]["fecha_nacimiento"] = None

    if 'hijos' in required_sections:
        while True:
            add_h = safe_input("\n¿Deseas agregar un hijo? (s/n): ").lower()
            if add_h != 's':
                break
            hijo = {}
            nombres_h = safe_input("Nombres del hijo/a: ", normalize=True)
            apellidos_h = safe_input("Apellidos del hijo/a: ", normalize=True)
            fecha_h = safe_input("Fecha de nacimiento del hijo/a (DD/MM/YYYY): ")
            hijo["nombres"] = [normalize_string(n) for n in nombres_h.split()] if nombres_h else []
            hijo["apellidos"] = [normalize_string(a) for a in apellidos_h.split()] if apellidos_h else []
            try:
                hijo["fecha_nacimiento"] = datetime.strptime(fecha_h, "%d/%m/%Y") if fecha_h else None
            except ValueError:
                hijo["fecha_nacimiento"] = None
            info["familia"]["hijos"].append(hijo)

    if 'otros' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Otros Datos Relevantes:")
        info["otros_datos"]["mascota"] = normalize_string(safe_input("Nombre de mascota: ", normalize=True))
        frases = safe_input("Palabras clave (SSID, etc. separadas por coma): ", normalize=True)
        info["otros_datos"]["frases"] = [normalize_string(p) for p in frases.split(',')] if frases else []
        nums = safe_input("Números importantes (n° de casa, etc. separados por coma): ")
        info["otros_datos"]["numeros_importantes"] = [p.strip() for p in nums.split(',')] if nums else []

    if 'mangle' in required_sections:
        frases_m = safe_input("Frases a 'destrozar' (ej: Red Segura) separadas por coma: ", normalize=True)
        info["otros_datos"]["mangle_phrases"] = [normalize_string(p) for p in frases_m.split(',')] if frases_m else []

    return info


def gather_numeric_info_interactive() -> List[str]:
    """
    Recopila números para modo numérico (interactivo).

    Returns:
        Lista de cadenas numéricas recopiladas
    """
    print(f"\n{Colors.CYAN}--- Recopilación de Datos para Generación Numérica ---{Colors.RESET}")
    numeric_data = set()

    rut = safe_input("RUT o DNI (sin puntos, con guión si aplica): ")
    if rut:
        numeric_data.add(normalize_string(rut).split('-')[0])

    print("\nFechas de Nacimiento (DD/MM/YYYY):")
    dates = []
    fecha = safe_input("  - Persona principal: ")
    if fecha:
        try:
            dates.append(datetime.strptime(fecha, "%d/%m/%Y"))
        except ValueError:
            pass
    fecha = safe_input("  - Pareja: ")
    if fecha:
        try:
            dates.append(datetime.strptime(fecha, "%d/%m/%Y"))
        except ValueError:
            pass

    child_count = 1
    while True:
        fecha = safe_input(f"  - Hijo/a {child_count}: ")
        if fecha:
            try:
                dates.append(datetime.strptime(fecha, "%d/%m/%Y"))
                child_count += 1
                continue
            except ValueError:
                pass
        otra = safe_input("¿Agregar otro hijo? (s/n): ").lower()
        if otra != 's':
            break

    for d in dates:
        numeric_data.update([str(d.day), f"{d.day:02d}", str(d.month), f"{d.month:02d}",
                            str(d.year), str(d.year)[2:], f"{d.day:02d}{d.month:02d}",
                            f"{d.month:02d}{d.day:02d}"])

    casa = safe_input("  - Número de casa/departamento: ")
    ult4 = safe_input("  - Últimos 4 dígitos del teléfono/tarjeta: ")
    if casa:
        numeric_data.add(casa.strip())
    if ult4:
        numeric_data.add(ult4.strip())

    return [n for n in numeric_data if n]


def gather_username_info_interactive() -> dict:
    """
    Recopila información para generación de nombres de usuario.

    Returns:
        Diccionario con nombres, apellidos, sobrenombre y año de nacimiento
    """
    print(f"\n{Colors.CYAN}--- Recopilación para nombres de usuario ---{Colors.RESET}")
    nombres = safe_input("Nombres (separados por espacio): ", normalize=True).lower()
    apellidos = safe_input("Apellidos (separados por espacio): ", normalize=True).lower()
    apodo = safe_input("Sobrenombre/Apodo: ", normalize=True).lower()
    birth = safe_input("Fecha de nacimiento (para usar el año): ")
    birth_year = None
    try:
        if birth:
            bd = datetime.strptime(birth, "%d/%m/%Y")
            birth_year = str(bd.year)
    except ValueError:
        birth_year = None

    return {
        'nombres': nombres.split() if nombres else [],
        'apellidos': apellidos.split() if apellidos else [],
        'sobrenombre': apodo or "",
        'birth_year': birth_year
    }


def generate_base_words(info: dict) -> List[str]:
    """
    Extrae palabras base desde la info (sin números).

    Args:
        info: Diccionario con información recopilada

    Returns:
        Lista ordenada de palabras base
    """
    words: Set[str] = set()

    def extract_words(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "fecha_nacimiento" and value:
                    # Añadir partes de la fecha (día, mes, año corto/largo)
                    words.add(str(value.day))
                    words.add(f"{value.day:02d}")
                    words.add(str(value.month))
                    words.add(f"{value.month:02d}")
                    words.add(str(value.year))
                    words.add(str(value.year)[2:])
                else:
                    extract_words(value)
        elif isinstance(data, list):
            for item in data:
                extract_words(item)
        elif isinstance(data, str) and data:
            for word in data.strip().lower().split():
                cleaned = normalize_string(word)
                if cleaned:
                    words.add(cleaned)

    extract_words(info)
    return sorted([w for w in words if not w.isdigit()])
