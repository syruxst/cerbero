import itertools
from datetime import datetime
import time
import sys
import os
import unicodedata

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

BANNER = f"""{Colors.MAGENTA}
██████╗ ███████╗██████╗ ██████╗ ███████╗██████╗  ██████╗ 
██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██═══██╗
██║      █████╗  ██████╔╝██████╔╝█████╗  ██████╔╝██║   ██║
██║      ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██╔══██╗██║   ██║
╚██████╗ ███████╗██║  ██║██████╔╝███████╗██║  ██║╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
    --- v5.3 ---
{Colors.RESET}"""

ETHICAL_DISCLAIMER = f"""{Colors.YELLOW}
[!] ADVERTENCIA DE USO ÉTICO:
Esta herramienta está diseñada exclusivamente para fines educativos y para ser utilizada
en auditorías de seguridad (pentesting) con autorización explícita del propietario del sistema.
El uso de esta herramienta en sistemas para los cuales no tienes permiso es ilegal.
El autor no se hace responsable por el mal uso de este programa.
{Colors.RESET}"""

LEETSPEAK_MAP = {'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['5', '$'], 't': ['7']}

def print_presentation():
    os.system('cls' if os.name == 'nt' else 'clear')
    for char in BANNER: sys.stdout.write(char); sys.stdout.flush(); time.sleep(0.001)
    print("\n" + "="*70 + f"\n {Colors.CYAN}Creado por: Daniel Ugalde{Colors.RESET}\n" + "="*70 + "\n")
    time.sleep(1)
    for line in ETHICAL_DISCLAIMER.splitlines(): print(line); time.sleep(0.05)
    print("\n" + "="*70 + "\n"); time.sleep(1)

def normalize_string(s): return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')

def get_input(prompt, allow_empty=True, normalize=False):
    full_prompt = f"{Colors.BLUE}{prompt}{Colors.RESET}"
    while True:
        value = input(full_prompt).strip()
        if value or allow_empty: return normalize_string(value) if normalize and value else value
        print(f"{Colors.YELLOW}Este campo no puede estar vacío.{Colors.RESET}")

def get_date_input(prompt):
    while True:
        date_str = get_input(prompt)
        if not date_str: return None
        try: return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError: print(f"{Colors.YELLOW}Formato de fecha inválido. Por favor, usa DD/MM/YYYY.{Colors.RESET}")

def save_wordlist(item_list, filename, list_type="contraseñas"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for item in sorted(item_list): f.write(item + '\n')
        print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} La lista de {list_type} se ha guardado en '{filename}'")
    except Exception as e: print(f"\n{Colors.RED}[ERROR]{Colors.RESET} No se pudo guardar el archivo: {e}")

def full_leetspeak(text):
    text = text.lower()
    for char, replacements in LEETSPEAK_MAP.items():
        if replacements: text = text.replace(char, replacements[0])
    return text

def gather_smart_information(required_sections):
    print(f"{Colors.CYAN}--- Recopilación de Información Personal (deja en blanco si no aplica) ---{Colors.RESET}")
    info = { "persona_principal": {}, "familia": {"pareja": {}, "hijos": []}, "otros_datos": {} }
    if 'principal' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Datos del objetivo principal:")
        info["persona_principal"]["nombres"] = [normalize_string(n) for n in get_input("Nombres (ej: José): ", normalize=True).split()]
        info["persona_principal"]["apellidos"] = [normalize_string(a) for a in get_input("Apellidos (ej: Núñez): ", normalize=True).split()]
        info["persona_principal"]["fecha_nacimiento"] = get_date_input("Fecha de nacimiento (DD/MM/YYYY): ")
        info["persona_principal"]["sobrenombre"] = get_input("Sobrenombre/Apodo: ", normalize=True)
    if 'pareja' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Datos de la Pareja:")
        info["familia"]["pareja"]["nombres"] = [normalize_string(n) for n in get_input("Nombres de la pareja: ", normalize=True).split()]
        info["familia"]["pareja"]["apellidos"] = [normalize_string(a) for a in get_input("Apellidos de la pareja: ", normalize=True).split()]
        info["familia"]["pareja"]["fecha_nacimiento"] = get_date_input("Fecha de nacimiento de la pareja (DD/MM/YYYY): ")
    if 'hijos' in required_sections:
        while True:
            if get_input("\n¿Deseas agregar un hijo? (s/n): ").lower() != 's': break
            hijo = {"nombres": [normalize_string(n) for n in get_input("Nombres del hijo/a: ", normalize=True).split()], "apellidos": [normalize_string(a) for a in get_input("Apellidos del hijo/a: ", normalize=True).split()], "fecha_nacimiento": get_date_input("Fecha de nacimiento del hijo/a (DD/MM/YYYY): ")}
            info["familia"]["hijos"].append(hijo)
    if 'otros' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Otros Datos Relevantes:")
        info["otros_datos"]["mascota"] = get_input("Nombre de mascota: ", normalize=True)
        info["otros_datos"]["frases"] = [normalize_string(p) for p in get_input("Palabras clave (SSID, etc.): ", normalize=True).split(',')]
        info["otros_datos"]["numeros_importantes"] = [p.strip() for p in get_input("Números importantes (n° de casa, etc.): ").split(',')]
    if 'mangle' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Datos para el Motor 'Mangler':")
        info["otros_datos"]["mangle_phrases"] = [normalize_string(p) for p in get_input("Frases a 'destrozar' (ej: Red Segura): ", normalize=True).split(',')]
    return info

def gather_numeric_info():
    print(f"\n{Colors.CYAN}--- Recopilación de Datos para Generación Numérica ---{Colors.RESET}"); numeric_data = set()
    rut = get_input("RUT o DNI (sin puntos, con guión si aplica): ")
    if rut: numeric_data.add(normalize_string(rut).split('-')[0])
    print("\nFechas de Nacimiento (DD/MM/YYYY):")
    dates = [get_date_input("  - Persona principal: "), get_date_input("  - Pareja: ")]
    child_count = 1
    while True:
        date = get_date_input(f"  - Hijo/a {child_count}: ")
        if date: dates.append(date); child_count += 1
        elif get_input("¿Agregar otro hijo? (s/n): ").lower() != 's': break
    for d in filter(None, dates):
        numeric_data.update([str(d.day), f"{d.day:02d}", str(d.month), f"{d.month:02d}", str(d.year), str(d.year)[2:], f"{d.day:02d}{d.month:02d}", f"{d.month:02d}{d.day:02d}"])
    print("\nOtros Números Relevantes:")
    numeric_data.add(get_input("  - Número de casa/departamento: "))
    numeric_data.add(get_input("  - Últimos 4 dígitos del teléfono/tarjeta: "))
    return list(filter(None, numeric_data))

def gather_username_info():
    print(f"\n{Colors.CYAN}--- Recopilación de Datos para Generación de Nombres de Usuario ---{Colors.RESET}"); info = {}
    info['nombres'] = get_input("Nombres (separados por espacio): ", normalize=True).lower().split()
    info['apellidos'] = get_input("Apellidos (separados por espacio): ", normalize=True).lower().split()
    info['sobrenombre'] = get_input("Sobrenombre/Apodo: ", normalize=True).lower()
    birth_date = get_date_input("Fecha de nacimiento (para usar el año): ")
    info['birth_year'] = str(birth_date.year) if birth_date else None
    return info

def generate_base_words(info):
    words = set()
    def extract_words(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "fecha_nacimiento" and value:
                    words.add(str(value.day)); words.add(f"{value.day:02d}"); words.add(str(value.month)); words.add(f"{value.month:02d}"); words.add(str(value.year)); words.add(str(value.year)[2:])
                else: extract_words(value)
        elif isinstance(data, list):
            for item in data: extract_words(item)
        elif isinstance(data, str) and data:
            for word in data.strip().lower().split(): words.add(word)
    extract_words(info)
    return list(filter(None, words))

def apply_variations(word):
    word = word.lower(); return list(set([word, word.capitalize(), word.upper()]))

def apply_mangling_rules(word):
    word = word.lower(); results = {word, word.upper(), word.capitalize()}
    if len(word) > 7:
        leet_word = full_leetspeak(word); results.update([leet_word, leet_word.capitalize(), leet_word.upper()]); return list(results)
    chars_to_replace = [(i, char) for i, char in enumerate(word) if char in LEETSPEAK_MAP]
    for i in range(1, len(chars_to_replace) + 1):
        for positions_combo in itertools.combinations(chars_to_replace, i):
            indices = [p[0] for p in positions_combo]; possible_replacements = [LEETSPEAK_MAP[p[1]] for p in positions_combo]
            for replacement_values in itertools.product(*possible_replacements):
                temp_word = list(word)
                for j, index in enumerate(indices): temp_word[index] = replacement_values[j]
                mangled_word = "".join(temp_word); results.update([mangled_word, mangled_word.capitalize(), mangled_word.upper()])
    return list(results)

def motor_1_combinaciones_simples(info, text_words, numeric_words, symbols, add_func):
    count = 0
    for text in text_words:
        for var in apply_variations(text):
            count += add_func(var)
            for num in numeric_words: count += add_func(f"{var}{num}")
    return count
def motor_2_patrones_complejos(info, text_words, numeric_words, symbols, add_func):
    count = 0; separators = ['-', '_', '.', '']
    for w1, w2 in itertools.permutations(text_words, 2):
        for var1 in apply_variations(w1):
            for var2 in apply_variations(w2):
                for sep in separators:
                    base = f"{var1}{sep}{var2}"; count += add_func(base)
                    for num in numeric_words:
                        for sym in symbols: count += add_func(f"{base}{sym}{num}")
    return count
def motor_3_leetspeak_moderno(info, text_words, numeric_words, symbols, add_func):
    count = 0; current_year = str(datetime.now().year); names = {n.lower() for n in info.get("persona_principal", {}).get("nombres", []) if n}
    if info.get("persona_principal", {}).get("sobrenombre"): names.add(info["persona_principal"]["sobrenombre"].lower())
    for name in names:
        if len(name) > 1:
            leet_base = f"{name[0].upper()}{full_leetspeak(name[1:])}"
            for sym in symbols:
                count += add_func(f"{current_year}{leet_base}{sym}"); count += add_func(f"{leet_base}{current_year}{sym}"); count += add_func(f"{leet_base}{sym}{current_year}")
    return count
def motor_4_centrado_en_hijos(info, text_words, numeric_words, symbols, add_func):
    count = 0
    for hijo in info.get("familia", {}).get("hijos", []):
        if hijo.get("fecha_nacimiento") and hijo.get("nombres"):
            year = str(hijo["fecha_nacimiento"].year)
            initials = "".join([n[0] for n in hijo["nombres"] if n] + [a[0] for a in hijo.get("apellidos", []) if a]).lower()
            if initials:
                initials_cased = initials.capitalize()
                for sym in symbols:
                    count += add_func(f"{year}{initials_cased}{sym}"); count += add_func(f"{initials_cased}{year}{sym}"); count += add_func(f"{initials_cased}{sym}{year}")
    return count
def motor_5_permutacion_iniciales(info, text_words, numeric_words, symbols, add_func):
    count = 0
    all_initials = [n[0] for n in info.get("persona_principal", {}).get("nombres", []) if n] + [n[0] for n in info.get("familia", {}).get("pareja", {}).get("nombres", []) if n] + [n[0] for h in info.get("familia", {}).get("hijos", []) for n in h.get("nombres", []) if n]
    key_numbers = set()
    all_dates = [info.get("persona_principal", {}).get("fecha_nacimiento"), info.get("familia", {}).get("pareja", {}).get("fecha_nacimiento")] + [h.get("fecha_nacimiento") for h in info.get("familia", {}).get("hijos", [])]
    for f_nac in filter(None, all_dates): key_numbers.update([f"{f_nac.day:02d}", str(f_nac.year)[2:]])
    if len(all_initials) < 2 or len(key_numbers) < 2: print(f"     {Colors.YELLOW}(Saltado: no hay suficientes iniciales o fechas){Colors.RESET}"); return 0
    for i in range(3, min(len(all_initials) + 1, 6)):
        for p_initials in itertools.permutations(all_initials, i):
            initial_part = "".join(p_initials); initial_part_cased = initial_part[0].upper() + initial_part[1:].lower()
            for p_numbers in itertools.permutations(key_numbers, 2):
                number_part = "".join(p_numbers); count += add_func(f"{initial_part_cased}{number_part}")
    return count
def motor_6_mangler_frases(info, text_words, numeric_words, symbols, add_func):
    count = 0; mangle_phrases = [p for p in info.get("otros_datos", {}).get("mangle_phrases", []) if p]
    if not mangle_phrases: print(f"     {Colors.YELLOW}(Saltado: no se proveyeron 'Frases a destrozar'){Colors.RESET}"); return 0
    years = {str(datetime.now().year)};
    if info.get("persona_principal", {}).get("fecha_nacimiento"): years.add(str(info["persona_principal"]["fecha_nacimiento"].year))
    complex_suffixes = ["!", "#", "!#", "@#", "!!", "*"]
    for phrase in mangle_phrases:
        words = phrase.strip().split()
        if len(words) == 2:
            w1, w2 = words; mangled1_list = apply_mangling_rules(w1); mangled2_list = apply_mangling_rules(w2)
            for m1 in mangled1_list:
                for m2 in mangled2_list:
                    base = f"{m1}{m2}"; count += add_func(base)
                    for year in years:
                        pass_year = f"{base}{year}"; count += add_func(pass_year)
                        for suffix in complex_suffixes: count += add_func(f"{pass_year}{suffix}")
    return count
def motor_7_combinatorio_creativo(info, text_words, numeric_words, symbols, add_func):
    count = 0
    if len(text_words) < 2 or len(numeric_words) < 1: print(f"     {Colors.YELLOW}(Saltado: no hay suficientes palabras o números){Colors.RESET}"); return 0
    for combo in itertools.permutations(text_words, 2):
        for num in numeric_words:
            w1, w2 = combo; var1_list = apply_variations(w1); var2_list = apply_variations(w2)
            for v1 in var1_list:
                for v2 in var2_list:
                    base = f"{v1}{v2}{num}"; count += add_func(base)
                    for s in symbols: count += add_func(f"{base}{s}")
                    base_sep = f"{v1}-{v2}{num}"; count += add_func(base_sep)
                    for s in symbols: count += add_func(f"{base_sep}{s}")
    return count
def motor_8_cadenas_biograficas(info, text_words, numeric_words, symbols, add_func):
    count = 0; people = []
    pareja = info.get("familia", {}).get("pareja", {})
    if pareja.get("nombres") and pareja.get("fecha_nacimiento"):
        people.append({"initial": pareja["nombres"][0][0], "year_short": str(pareja["fecha_nacimiento"].year)[2:]})
    for hijo in info.get("familia", {}).get("hijos", []):
        if hijo.get("nombres") and hijo.get("fecha_nacimiento"):
            people.append({"initial": hijo["nombres"][0][0], "year_short": str(hijo["fecha_nacimiento"].year)[2:]})
    if len(people) < 2: print(f"     {Colors.YELLOW}(Saltado: no hay suficientes 'pares biográficos'){Colors.RESET}"); return 0
    for length in range(2, len(people) + 1):
        for p_people in itertools.permutations(people, length):
            chunk_variations_for_permutation = []
            for person in p_people:
                initial_lower = person['initial'].lower(); initial_upper = person['initial'].upper(); year = person['year_short']
                chunk_variations_for_permutation.append([f"{initial_lower}{year}", f"{initial_upper}{year}"])
            for combo in itertools.product(*chunk_variations_for_permutation): count += add_func("".join(combo))
    return count

def generate_full_passwords(info, base_words, min_len, max_len, engines_to_run, dry_run):
    passwords = set(); stats = {}
    def add_password(p):
        if min_len <= len(p) <= max_len:
            if not dry_run: passwords.add(p)
            return 1
        return 0
    text_words = [word for word in base_words if not word.isdigit()]; numeric_words = [word for word in base_words if word.isdigit()]; symbols = ['$', '#', '!', '*', '.', '&', '%', '@', '/']
    engine_functions = {'1': motor_1_combinaciones_simples, '2': motor_2_patrones_complejos, '3': motor_3_leetspeak_moderno, '4': motor_4_centrado_en_hijos, '5': motor_5_permutacion_iniciales, '6': motor_6_mangler_frases, '7': motor_7_combinatorio_creativo, '8': motor_8_cadenas_biograficas}
    total_count = 0; total_start_time = time.time()
    for engine_id in sorted(engine_functions.keys()):
        if 'all' in engines_to_run or engine_id in engines_to_run:
            start_time = time.time(); engine_name = engine_functions[engine_id].__name__.replace('_', ' ').replace('motor ', 'Motor '); print(f"  {Colors.CYAN}->{Colors.RESET} {engine_name}...")
            count = engine_functions[engine_id](info, text_words, numeric_words, symbols, add_password); end_time = time.time()
            total_count += count; stats[engine_name] = {'count': count, 'time': end_time - start_time}
    total_end_time = time.time(); stats['Total'] = {'count': total_count if dry_run else len(passwords), 'time': total_end_time - total_start_time}
    if dry_run: return total_count, stats
    return list(passwords), stats

def generate_usernames(info):
    if not info['nombres'] or not info['apellidos']: print(f"{Colors.YELLOW}[AVISO] Se necesita al menos un nombre y un apellido.{Colors.RESET}"); return []
    fname, lname, nickname, usernames = info['nombres'][0], info['apellidos'][0], info['sobrenombre'], set()
    patterns = [fname, lname, nickname, f"{fname}{lname}", f"{lname}{fname}", f"{fname[0]}{lname}", f"{fname}{lname[0]}"]
    if nickname: patterns.extend([f"{nickname}{lname}", f"{fname}{nickname}"])
    for p in patterns:
        if p: usernames.add(p)
    separators = ['.', '_', '-']
    for sep in separators: usernames.add(f"{fname}{sep}{lname}"); usernames.add(f"{fname[0]}{sep}{lname}")
    numeric_suffixes = []
    if info['birth_year']: numeric_suffixes.extend([info['birth_year'], info['birth_year'][2:]])
    numeric_suffixes.append(str(datetime.now().year)[2:])
    base_usernames = list(usernames)
    for user in base_usernames:
        for suffix in numeric_suffixes: usernames.add(f"{user}{suffix}")
    return list(filter(None, usernames))

def run_full_mode():
    print(f"\n{Colors.CYAN}--- MODO COMPLETO: WORDLIST AVANZADA ---{Colors.RESET}\n")
    engine_dependencies = {'1': ['principal', 'pareja', 'hijos', 'otros', 'familia'], '2': ['principal', 'pareja', 'hijos', 'otros', 'familia'], '3': ['principal'], '4': ['hijos'], '5': ['principal', 'pareja', 'hijos'], '6': ['mangle', 'principal'], '7': ['principal', 'pareja', 'hijos', 'otros', 'familia'], '8': ['pareja', 'hijos']}
    print("Motores de Generación Disponibles:")
    print("  1. Combinaciones simples (ej: maria1995)")
    print("  2. Patrones complejos (ej: juan-perez/92)")
    print("  3. Leetspeak moderno (ej: 2025R0b3rt0!)")
    print("  4. Centrado en Hijos (ej: 2018Sgl#)")
    print("  5. Permutación de iniciales (ej: Pml2590)")
    print("  6. 'Mangler' de frases (ej: M1Cl4v32024*)")
    print("  7. Combinatorio creativo (ej: Amor-Ana99!)")
    print(f"  8. Cadenas biográficas (ej: C80l05m10)")    
    engines_input = get_input("¿Qué motores deseas ejecutar? (ej: 1,3,8 o 'all' para todos) [all]: ") or "all"
    engines_to_run = [e.strip() for e in engines_input.lower().split(',')]
    required_sections = set()
    if 'all' in engines_to_run: required_sections = {'principal', 'pareja', 'hijos', 'otros', 'mangle', 'familia'}
    else:
        for eng in engines_to_run:
            if eng in engine_dependencies: required_sections.update(engine_dependencies[eng])
    dry_run_input = get_input(f"¿Ejecutar en modo simulación (dry run)? {Colors.YELLOW}*** NOTA: Esto no generará una lista ***{Colors.RESET} (s/n) [n]: ").lower()
    dry_run = True if dry_run_input == 's' else False
    info = gather_smart_information(required_sections)
    base_words = generate_base_words(info)
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se encontraron {len(base_words)} palabras base.")
    try: min_length = int(get_input("Introduce la longitud MÍNIMA [8]: ") or 8); max_length = int(get_input("Introduce la longitud MÁXIMA [16]: ") or 16)
    except ValueError: min_length, max_length = 8, 16; print(f"{Colors.YELLOW}Entrada inválida. Usando rango por defecto {min_length}-{max_length}.{Colors.RESET}")
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Ejecutando motores de generación de contraseñas...");
    result, stats = generate_full_passwords(info, base_words, min_length, max_length, engines_to_run, dry_run)
    print(f"\n{Colors.CYAN}--- ESTADÍSTICAS DE GENERACIÓN ---{Colors.RESET}")
    for engine, data in stats.items():
        if engine == "Total": continue
        print(f"  - {engine}: {Colors.GREEN}{data['count']:,}{Colors.RESET} candidatas en {data['time']:.2f} segundos.")
    print("------------------------------------")
    total_data = stats.get('Total', {'count': 0, 'time': 0})
    if dry_run:
        print(f"\n{Colors.YELLOW}[ESTIMACIÓN]{Colors.RESET} El proceso generaría un total de {Colors.GREEN}{total_data['count']:,}{Colors.RESET} contraseñas.")
        print(f"Tiempo total estimado: {total_data['time']:.2f} segundos.")
    else:
        password_list = result
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se generaron {Colors.GREEN}{len(password_list):,}{Colors.RESET} contraseñas únicas en total.")
        print(f"Tiempo total de generación: {total_data['time']:.2f} segundos.")
        if not password_list: print(f"{Colors.YELLOW}[AVISO] No se generaron contraseñas.{Colors.RESET}"); return
        output_filename = get_input("\nIntroduce el nombre del archivo de salida (ej: wordlist.txt): ", allow_empty=False)
        save_wordlist(password_list, output_filename, "contraseñas")

def run_numeric_mode():
    print(f"\n{Colors.CYAN}--- MODO NUMÉRICO: PINS / CÓDIGOS ---{Colors.RESET}\n"); base_numbers = gather_numeric_info()
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se recopilaron {len(base_numbers)} piezas de datos numéricos.")
    try:
        min_len = int(get_input("Longitud numérica MÍNIMA [4]: ") or 4)
        max_len = int(get_input("Longitud numérica MÁXIMA [12]: ") or 12)
    except ValueError:
        print(f"{Colors.YELLOW}Entrada inválida. Usando rango por defecto 4-12.{Colors.RESET}"); min_len, max_len = 4, 12
    print(f"{Colors.YELLOW}[INFO]{Colors.RESET} Generando combinaciones numéricas..."); passwords = set()
    for num in base_numbers:
        if min_len <= len(num) <= max_len: passwords.add(num)
    for r in range(2, 4):
        for combo in itertools.permutations(base_numbers, r):
            password = "".join(combo)
            if min_len <= len(password) <= max_len: passwords.add(password)
    print(f"{Colors.GREEN}[+]{Colors.RESET} Se generaron {len(passwords)} códigos numéricos únicos en el rango de {min_len}-{max_len} dígitos.")
    output_filename = get_input("\nIntroduce el nombre del archivo de salida (ej: wordlist_numeric.txt): ", allow_empty=False)
    save_wordlist(list(passwords), output_filename, "códigos numéricos")
    
def run_username_mode():
    print(f"\n{Colors.CYAN}--- MODO GENERADOR DE NOMBRES DE USUARIO ---{Colors.RESET}\n"); info = gather_username_info()
    username_list = generate_usernames(info)
    if username_list:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se generaron {len(username_list)} nombres de usuario potenciales.")
        output_filename = get_input("\nIntroduce el nombre del archivo de salida (ej: userlist.txt): ", allow_empty=False)
        save_wordlist(username_list, output_filename, "nombres de usuario")

def run_audit_mode():
    print(f"\n{Colors.CYAN}--- MODO AUDITORÍA: BUSCAR CONTRASEÑA EN WORDLIST ---{Colors.RESET}\n")
    file_path = get_input("Introduce la ruta del archivo de la wordlist a revisar: ")
    if not os.path.exists(file_path):
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} El archivo '{file_path}' no se encontró."); return
    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Wordlist '{file_path}' cargada. Puedes empezar a auditar.")
    while True:
        password_to_check = get_input("\nIntroduce la contraseña a verificar (o presiona Enter para volver al menú): ")
        if not password_to_check: break
        print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Buscando la contraseña en '{file_path}'..."); found = False
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.strip() == password_to_check: found = True; break
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Ocurrió un error al leer el archivo: {e}"); return
        print("-" * 50)
        if found:
            print(f"{Colors.RED}[!!!] ALERTA DE SEGURIDAD [!!!]{Colors.RESET}")
            print("Tu contraseña FUE ENCONTRADA en la lista.")
            print("Esto significa que es predecible y altamente insegura.")
            print(f"{Colors.YELLOW}==> RECOMENDACIÓN: ¡Cámbiala inmediatamente por una más compleja! <==")
        else:
            print(f"{Colors.GREEN}[✓] BUENA NOTICIA [✓]{Colors.RESET}")
            print("Tu contraseña NO FUE ENCONTRADA en esta wordlist.")
            print("Es una buena señal, pero recuerda mantener siempre buenas prácticas de seguridad.")
        print(f"{Colors.RESET}{'-' * 50}")

def run_merge_mode():
    print(f"\n{Colors.CYAN}--- MODO UNIR WORDLISTS ---{Colors.RESET}\n")
    input_files_str = get_input("Introduce las rutas de los archivos a unir (separadas por coma): ")
    if not input_files_str:
        print(f"{Colors.YELLOW}[AVISO]{Colors.RESET} No se especificaron archivos."); return
    file_paths = [path.strip() for path in input_files_str.split(',')]
    unique_passwords = set(); total_lines_read = 0
    print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Procesando archivos...")
    for path in file_paths:
        if not os.path.exists(path):
            print(f"  {Colors.YELLOW}[AVISO]{Colors.RESET} El archivo '{path}' no se encontró y será omitido.")
            continue
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
                unique_passwords.update(lines); total_lines_read += len(lines)
                print(f"  {Colors.GREEN}[+]{Colors.RESET} Procesado '{path}', leídas {len(lines):,} líneas.")
        except Exception as e:
            print(f"  {Colors.RED}[ERROR]{Colors.RESET} No se pudo leer el archivo '{path}': {e}")
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Total de líneas leídas: {total_lines_read:,}")
    print(f"{Colors.GREEN}[+]{Colors.RESET} Total de contraseñas únicas encontradas: {len(unique_passwords):,}")
    if not unique_passwords:
        print(f"{Colors.YELLOW}[AVISO]{Colors.RESET} No se encontraron contraseñas para guardar."); return
    output_filename = get_input("\nIntroduce el nombre del archivo de salida para la lista unificada: ", allow_empty=False)
    save_wordlist(list(unique_passwords), output_filename, "contraseñas unificadas")

def main():
    print_presentation()
    try:
        while True:
            print(f"\n{Colors.CYAN}Selecciona un modo de operación:{Colors.RESET}")
            print(f"  {Colors.YELLOW}1.{Colors.RESET} Modo Completo (Generar Wordlist Avanzada)")
            print(f"  {Colors.YELLOW}2.{Colors.RESET} Modo Numérico (Generar PINs / Códigos)")
            print(f"  {Colors.YELLOW}3.{Colors.RESET} Modo Nombres de Usuario (Generar Userlist)")
            print(f"  {Colors.YELLOW}4.{Colors.RESET} Modo Auditoría (Buscar tu contraseña en una lista)")
            print(f"  {Colors.YELLOW}5.{Colors.RESET} Modo Unir Wordlists (Combinar múltiples listas en una)")
            print(f"  {Colors.YELLOW}6.{Colors.RESET} Salir")
            choice = get_input("Opción: ")
            if choice == '1': run_full_mode()
            elif choice == '2': run_numeric_mode()
            elif choice == '3': run_username_mode()
            elif choice == '4': run_audit_mode()
            elif choice == '5': run_merge_mode()
            elif choice == '6': print(f"\n{Colors.CYAN}Saliendo de Cerbero. ¡Hasta la próxima!{Colors.RESET}"); break
            else: print(f"{Colors.YELLOW}Opción no válida.{Colors.RESET}")
            if choice in ['1', '2', '3', '4', '5']: get_input("\nPresiona Enter para volver al menú principal...")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[INFO]{Colors.RESET} Salida solicitada por el usuario. ¡Gracias por usar Cerbero!")
        sys.exit(0)



if __name__ == "__main__":
    main()