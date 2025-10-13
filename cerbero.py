import itertools
from datetime import datetime
import time
import sys
import os

BANNER = """
██████╗ ███████╗██████╗ ██████╗ ███████╗██████╗  ██████╗ 
██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔═══██╗
██║      █████╗  ██████╔╝██████╔╝█████╗  ██████╔╝██║   ██║
██║      ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██╔══██╗██║   ██║
╚██████╗ ███████╗██║  ██║██████╔╝███████╗██║  ██║╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
    --- Permutation Engine Edition v2.8 ---
"""

ETHICAL_DISCLAIMER = """
[!] ADVERTENCIA DE USO ÉTICO:
Esta herramienta está diseñada exclusivamente para fines educativos y para ser utilizada
en auditorías de seguridad (pentesting) con autorización explícita del propietario del sistema.
El uso de esta herramienta en sistemas para los cuales no tienes permiso es ilegal.
El autor no se hace responsable por el mal uso de este programa.
"""

# --- FUNCIONES GLOBALES Y UTILIDADES ---
LEETSPEAK_MAP = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7', 'g': '6', 'b': '8'}

def print_presentation():
    for char in BANNER: sys.stdout.write(char); sys.stdout.flush(); time.sleep(0.002)
    print("\n" + "="*70 + "\n Creado por: Daniel Ugalde\n" + "="*70 + "\n")
    time.sleep(1)
    for line in ETHICAL_DISCLAIMER.splitlines(): print(line); time.sleep(0.05)
    print("\n" + "="*70 + "\n"); time.sleep(1)

def get_input(prompt, allow_empty=True):
    while True:
        value = input(prompt).strip()
        if value or allow_empty: return value
        print("Este campo no puede estar vacío.")

def get_date_input(prompt):
    while True:
        date_str = get_input(prompt)
        if not date_str: return None
        try: return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError: print("Formato de fecha inválido. Por favor, usa DD/MM/YYYY.")

def save_wordlist(item_list, filename, list_type="contraseñas"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for item in sorted(item_list): f.write(item + '\n')
        print(f"\n[SUCCESS] La lista de {list_type} se ha guardado en '{filename}'")
    except Exception as e: print(f"\n[ERROR] No se pudo guardar el archivo: {e}")

def full_leetspeak(text):
    text = text.lower()
    for char, replacement in LEETSPEAK_MAP.items(): text = text.replace(char, replacement)
    return text

# --- MODO 1: WORDLIST COMPLETA ---
def gather_full_information():
    # (Sin cambios en esta función)
    print("--- Recopilación de Información Personal (deja en blanco si no aplica) ---")
    info = { "persona_principal": {}, "familia": {"padre": {}, "madre": {}, "pareja": {}, "hijos": []}, "otros_datos": {} }
    print("\n[+] Datos del objetivo principal:"); info["persona_principal"]["nombres"] = get_input("Nombres: ").split(); info["persona_principal"]["apellidos"] = get_input("Apellidos: ").split(); info["persona_principal"]["fecha_nacimiento"] = get_date_input("Fecha de nacimiento (DD/MM/YYYY): "); info["persona_principal"]["sobrenombre"] = get_input("Sobrenombre/Apodo: "); info["persona_principal"]["telefono"] = get_input("Número de teléfono: "); info["persona_principal"]["correo"] = get_input("Correo electrónico: ")
    print("\n[+] Datos del Padre:"); info["familia"]["padre"]["nombres"] = get_input("Nombres del padre: ").split()
    print("\n[+] Datos de la Madre:"); info["familia"]["madre"]["nombres"] = get_input("Nombres de la madre: ").split()
    print("\n[+] Datos de la Pareja:"); info["familia"]["pareja"]["nombres"] = get_input("Nombres de la pareja: ").split(); info["familia"]["pareja"]["apellidos"] = get_input("Apellidos de la pareja: ").split(); info["familia"]["pareja"]["fecha_nacimiento"] = get_date_input("Fecha de nacimiento de la pareja (DD/MM/YYYY): ")
    while True:
        if get_input("\n¿Deseas agregar un hijo? (s/n): ").lower() != 's': break
        hijo = {"nombres": get_input("Nombres del hijo/a: ").split(), "apellidos": get_input("Apellidos del hijo/a: ").split(), "fecha_nacimiento": get_date_input("Fecha de nacimiento del hijo/a (DD/MM/YYYY): ")}
        info["familia"]["hijos"].append(hijo)
    print("\n[+] Otros Datos Relevantes:"); info["otros_datos"]["mascota"] = get_input("Nombre de mascota: "); info["otros_datos"]["frases"] = get_input("Frases o palabras clave (SSID de WiFi, etc. Separadas por coma): ").split(','); info["otros_datos"]["numeros_importantes"] = get_input("Números importantes (n° de casa, código postal, etc. Separados por coma): ").split(','); info["otros_datos"]["pelicula_favorita"] = get_input("Película favorita: "); info["otros_datos"]["hobby"] = get_input("Hobby o pasatiempo: "); info["otros_datos"]["musica"] = get_input("Música o banda favorita: ")
    return info

def generate_base_words(info):
    # (Función corregida de la v2.7.1)
    words = set()
    def extract_words(data):
        if isinstance(data, dict):
            for value in data.values(): extract_words(value)
        elif isinstance(data, list):
            for item in data: extract_words(item)
        elif isinstance(data, str) and data:
            cleaned_item = data.strip()
            if cleaned_item:
                for word in cleaned_item.lower().split(): words.add(word)
    extract_words(info)
    def get_initials(nombres, apellidos): return "".join([n[0] for n in nombres if n] + [a[0] for a in apellidos if a]).lower()
    if info["persona_principal"]["nombres"]: words.add(get_initials(info["persona_principal"]["nombres"], info["persona_principal"]["apellidos"]))
    for hijo in info["familia"]["hijos"]:
        if hijo["nombres"]: words.add(get_initials(hijo["nombres"], hijo["apellidos"]))
    def extract_date_parts(date_obj):
        if not date_obj: return
        words.update([str(date_obj.day), f"{date_obj.day:02d}", str(date_obj.month), f"{date_obj.month:02d}", str(date_obj.year), str(date_obj.year)[2:]])
    extract_date_parts(info["persona_principal"]["fecha_nacimiento"]); extract_date_parts(info["familia"]["pareja"]["fecha_nacimiento"])
    for hijo in info["familia"]["hijos"]: extract_date_parts(hijo["fecha_nacimiento"])
    return list(filter(None, words))

def apply_variations(word):
    return list(set([word, word.capitalize(), word.upper()]))

def generate_full_passwords(info, base_words):
    passwords = set()
    
    # ... (lógicas de generación anteriores) ...
    for w1, w2 in itertools.permutations(base_words, 2):
        for var1 in apply_variations(w1):
            for var2 in apply_variations(w2):
                passwords.add(f"{var1}{var2}")

    # *** NUEVA LÓGICA: Motor de Permutación de Iniciales + Números ***
    all_initials = []
    # Recolectar iniciales de todos los nombres (permitiendo repeticiones)
    for nombre in info["persona_principal"]["nombres"]: all_initials.append(nombre[0])
    for nombre in info["familia"]["pareja"]["nombres"]: all_initials.append(nombre[0])
    for hijo in info["familia"]["hijos"]:
        for nombre in hijo["nombres"]: all_initials.append(nombre[0])

    # Recolectar números clave
    key_numbers = []
    if info["persona_principal"]["fecha_nacimiento"]:
        f_nac = info["persona_principal"]["fecha_nacimiento"]
        key_numbers.extend([str(f_nac.day), str(f_nac.year)[2:]])

    if len(all_initials) >= 2 and len(key_numbers) >= 2:
        # 1. Generar la parte de iniciales (ej. Cdck)
        # Generamos permutaciones de un tamaño razonable (ej. de 3 a 5 iniciales)
        for i in range(3, min(len(all_initials) + 1, 6)):
            for p_initials in itertools.permutations(all_initials, i):
                initial_part = "".join(p_initials)
                # Aplicar la regla de la primera mayúscula
                initial_part_cased = initial_part[0].upper() + initial_part[1:].lower()

                # 2. Generar la parte numérica (ej. 1277)
                for p_numbers in itertools.permutations(key_numbers, len(key_numbers)):
                    number_part = "".join(p_numbers)

                    # 3. Combinar todo
                    # Patrón: Iniciales + Números
                    passwords.add(f"{initial_part_cased}{number_part}")
                    # Patrón: Números + Iniciales
                    passwords.add(f"{number_part}{initial_part_cased}")
                    
                    # Patrón complejo como el del ejemplo: Iniciales + Números + Iniciales
                    # Tomamos las iniciales restantes para la parte final
                    remaining_initials = list(all_initials)
                    for char in p_initials: remaining_initials.remove(char)
                    
                    if len(remaining_initials) > 1:
                        for p_rem_initials in itertools.permutations(remaining_initials, 2):
                            final_part = "".join(p_rem_initials).lower()
                            passwords.add(f"{initial_part_cased}{number_part}{final_part}")


    # ... (resto de las lógicas) ...
    return list(passwords)

def run_full_mode():
    print("\n--- MODO COMPLETO: WORDLIST AVANZADA ---\n"); info = gather_full_information()
    print("\n[+] Generando palabras base..."); base_words = generate_base_words(info)
    print(f"Se encontraron {len(base_words)} palabras base.")
    print("[+] Generando la lista de contraseñas..."); password_list = generate_full_passwords(info, base_words)
    total_generated = len(password_list)
    print(f"Se generaron {total_generated} contraseñas candidatas.")
    try:
        min_length = int(get_input("Introduce la longitud MÍNIMA de las contraseñas [8]: ") or 8)
        max_length = int(get_input("Introduce la longitud MÁXIMA de las contraseñas [12]: ") or 12)
    except ValueError: min_length, max_length = 8, 12; print(f"Entrada inválida. Usando rango por defecto {min_length}-{max_length}.")
    filtered_passwords = [p for p in password_list if min_length <= len(p) <= max_length]
    print(f"[+] Filtrando... {len(filtered_passwords)} de {total_generated} contraseñas cumplen con el rango de longitud.")
    output_filename = get_input("\nIntroduce el nombre del archivo de salida (ej: wordlist_full.txt): ", allow_empty=False)
    save_wordlist(filtered_passwords, output_filename, "contraseñas")

# --- MODO 2, 3, 4 y MAIN (sin cambios) ---
# (El resto del código es idéntico a la versión anterior)
def gather_numeric_info():
    print("\n--- Recopilación de Datos para Generación Numérica ---"); numeric_data = set()
    rut = get_input("RUT o DNI (sin puntos, con guión si aplica. Ej: 12345678-9): ")
    if rut: numeric_data.add(rut.split('-')[0])
    print("\nFechas de Nacimiento (DD/MM/YYYY):")
    dates = [get_date_input("  - Persona principal: "), get_date_input("  - Pareja: ")]
    child_count = 1
    while True:
        date = get_date_input(f"  - Hijo/a {child_count}: ");
        if date: dates.append(date); child_count += 1
        elif get_input("¿Agregar otro hijo? (s/n): ").lower() != 's': break
    for d in filter(None, dates): numeric_data.update([str(d.day), f"{d.day:02d}", str(d.month), f"{d.month:02d}", str(d.year), str(d.year)[2:], f"{d.day:02d}{d.month:02d}", f"{d.month:02d}{d.day:02d}"])
    print("\nOtros Números Relevantes:"); numeric_data.add(get_input("  - Número de casa/departamento: ")); numeric_data.add(get_input("  - Últimos 4 dígitos del teléfono/tarjeta: "))
    return list(filter(None, numeric_data))
def run_numeric_mode():
    print("\n--- MODO NUMÉRICO: PINS / CÓDIGOS ---\n"); base_numbers = gather_numeric_info()
    print(f"\n[+] Se recopilaron {len(base_numbers)} piezas de datos numéricos.")
    try: min_len = int(get_input("Longitud numérica MÍNIMA [4]: ") or 4); max_len = int(get_input("Longitud numérica MÁXIMA [12]: ") or 12)
    except ValueError: print("Entrada inválida. Usando rango por defecto 4-12."); min_len, max_len = 4, 12
    print("[+] Generando combinaciones numéricas..."); passwords = set()
    for num in base_numbers:
        if min_len <= len(num) <= max_len: passwords.add(num)
    for r in range(2, 4):
        for combo in itertools.permutations(base_numbers, r):
            password = "".join(combo)
            if min_len <= len(password) <= max_len: passwords.add(password)
    print(f"[+] Se generaron {len(passwords)} códigos numéricos únicos en el rango de {min_len}-{max_len} dígitos.")
    output_filename = get_input("\nIntroduce el nombre del archivo de salida (ej: wordlist_numeric.txt): ", allow_empty=False)
    save_wordlist(list(passwords), output_filename, "códigos numéricos")
def gather_username_info():
    print("\n--- Recopilación de Datos para Generación de Nombres de Usuario ---"); info = {}
    info['nombres'] = get_input("Nombres (separados por espacio): ").lower().split(); info['apellidos'] = get_input("Apellidos (separados por espacio): ").lower().split(); info['sobrenombre'] = get_input("Sobrenombre/Apodo: ").lower()
    birth_date = get_date_input("Fecha de nacimiento (para usar el año): "); info['birth_year'] = str(birth_date.year) if birth_date else None
    return info
def generate_usernames(info):
    if not info['nombres'] or not info['apellidos']: print("[AVISO] Se necesita al menos un nombre y un apellido para generar la lista."); return []
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
def run_username_mode():
    print("\n--- MODO GENERADOR DE NOMBRES DE USUARIO ---\n"); info = gather_username_info(); username_list = generate_usernames(info)
    if username_list:
        print(f"\n[+] Se generaron {len(username_list)} nombres de usuario potenciales.")
        output_filename = get_input("Introduce el nombre del archivo de salida (ej: userlist.txt): ", allow_empty=False)
        save_wordlist(username_list, output_filename, "nombres de usuario")
def run_audit_mode():
    print("\n--- MODO AUDITORÍA: BUSCAR CONTRASEÑA EN WORDLIST ---\n")
    file_path = get_input("Introduce la ruta del archivo de la wordlist a revisar: ", allow_empty=False)
    if not os.path.exists(file_path): print(f"\n[ERROR] El archivo '{file_path}' no se encontró."); return
    password_to_check = get_input("Introduce la contraseña que deseas verificar: ", allow_empty=False)
    print(f"\n[INFO] Buscando la contraseña en '{file_path}'..."); found = False
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip() == password_to_check: found = True; break
    except Exception as e: print(f"\n[ERROR] Ocurrió un error al leer el archivo: {e}"); return
    print("-" * 50)
    if found: print("[!!!] ALERTA DE SEGURIDAD [!!!]\nTu contraseña FUE ENCONTRADA en la lista.\nEsto significa que es predecible y altamente insegura.\n==> RECOMENDACIÓN: ¡Cámbiala inmediatamente por una más compleja! <==")
    else: print("[✓] BUENA NOTICIA [✓]\nTu contraseña NO FUE ENCONTRADA en esta wordlist.\nEs una buena señal, pero recuerda mantener siempre buenas prácticas de seguridad.")
    print("-" * 50)
def main():
    print_presentation()
    while True:
        print("\nSelecciona un modo de operación:")
        print("  1. Modo Completo (Generar Wordlist de Contraseñas)")
        print("  2. Modo Numérico (Generar PINs / Códigos)")
        print("  3. Modo Nombres de Usuario (Generar Userlist)")
        print("  4. Modo Auditoría (Buscar tu contraseña en una lista)")
        print("  5. Salir")
        choice = get_input("Opción: ")
        if choice == '1': run_full_mode()
        elif choice == '2': run_numeric_mode()
        elif choice == '3': run_username_mode()
        elif choice == '4': run_audit_mode()
        elif choice == '5': print("Saliendo de Cerbero. ¡Hasta la próxima!"); break
        else: print("Opción no válida. Por favor, elige una de las opciones.")
        if choice in ['1', '2', '3', '4']: input("\nPresiona Enter para volver al menú principal...")

if __name__ == "__main__":
    main()