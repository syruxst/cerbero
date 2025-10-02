import itertools
from datetime import datetime
import time
import sys

# --- PRESENTACIÓN DE LA HERRAMIENTA ---

BANNER = """
██████╗ ███████╗██████╗ ██████╗ ███████╗ ██████╗  ██████╗ 
██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔═══██╗
██║      █████╗  ██████╔╝██████╔╝█████╗  ██║   ██║██║   ██║
██║      ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██║   ██║██║   ██║
╚██████╗ ███████╗██║  ██║██████╔╝███████╗╚██████╔╝╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ 
        --- Advanced Wordlist Generator for Pentesters ---
"""

ETHICAL_DISCLAIMER = """
[!] ADVERTENCIA DE USO ÉTICO:
Esta herramienta está diseñada exclusivamente para fines educativos y para ser utilizada
en auditorías de seguridad (pentesting) con autorización explícita del propietario del sistema.
El uso de esta herramienta en sistemas para los cuales no tienes permiso es ilegal.
El autor no se hace responsable por el mal uso de este programa.
"""

def print_presentation():
    """Imprime el banner y el disclaimer con un efecto de escritura."""
    for char in BANNER:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.001)
    
    print("\n" + "="*70)
    print("                Creado por: Daniel Ugalde")
    print("="*70 + "\n")
    time.sleep(1)
    
    for line in ETHICAL_DISCLAIMER.splitlines():
        print(line)
        time.sleep(0.05)
    print("\n" + "="*70 + "\n")
    time.sleep(2)

# --- FIN DE LA PRESENTACIÓN ---

# Diccionario para sustituciones Leetspeak
LEETSPEAK_MAP = {
    'a': ['4', '@'],
    'A': ['4', '@'],
    'e': ['3'],
    'E': ['3'],
    'i': ['1', '!'],
    'I': ['1', '!'],
    'o': ['0'],
    'O': ['0'],
    's': ['5', '$'],
    'S': ['5', '$'],
    't': ['7'],
    'T': ['7']
}

def get_input(prompt, allow_empty=True):
    """Función para obtener la entrada del usuario de forma segura."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Este campo no puede estar vacío.")

def get_date_input(prompt):
    """Función para obtener y validar una fecha."""
    while True:
        date_str = get_input(prompt)
        if not date_str:
            return None
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            return date_obj
        except ValueError:
            print("Formato de fecha inválido. Por favor, usa DD/MM/YYYY.")

def gather_information():
    """Recopila toda la información personal a través de preguntas interactivas."""
    print("--- Recopilación de Información Personal (deja en blanco si no aplica) ---")
    info = {
        "persona_principal": {},
        "familia": {"padre": {}, "madre": {}, "pareja": {}, "hijos": []},
        "otros_datos": {}
    }
    # ... (El resto de la función de recopilación de datos no cambia) ...
    # Datos de la persona principal
    print("\n[+] Datos del objetivo principal:")
    info["persona_principal"]["nombres"] = get_input("Nombres: ").split()
    info["persona_principal"]["apellidos"] = get_input("Apellidos: ").split()
    info["persona_principal"]["fecha_nacimiento"] = get_date_input("Fecha de nacimiento (DD/MM/YYYY): ")
    info["persona_principal"]["sobrenombre"] = get_input("Sobrenombre/Apodo: ")
    info["persona_principal"]["telefono"] = get_input("Número de teléfono: ")
    info["persona_principal"]["correo"] = get_input("Correo electrónico: ")

    # Datos familiares
    print("\n[+] Datos del Padre:")
    info["familia"]["padre"]["nombres"] = get_input("Nombres del padre: ").split()
    
    print("\n[+] Datos de la Madre:")
    info["familia"]["madre"]["nombres"] = get_input("Nombres de la madre: ").split()

    print("\n[+] Datos de la Pareja:")
    info["familia"]["pareja"]["nombres"] = get_input("Nombres de la pareja: ").split()
    info["familia"]["pareja"]["apellidos"] = get_input("Apellidos de la pareja: ").split()

    # Datos de los hijos
    while True:
        add_child = get_input("\n¿Deseas agregar un hijo? (s/n): ").lower()
        if add_child != 's':
            break
        hijo = {}
        hijo["nombres"] = get_input("Nombres del hijo/a: ").split()
        hijo["apellidos"] = get_input("Apellidos del hijo/a: ").split()
        hijo["fecha_nacimiento"] = get_date_input("Fecha de nacimiento del hijo/a (DD/MM/YYYY): ")
        info["familia"]["hijos"].append(hijo)

    # Otros datos
    print("\n[+] Otros Datos Relevantes:")
    info["otros_datos"]["mascota"] = get_input("Nombre de mascota: ")
    info["otros_datos"]["frases"] = get_input("Frases o palabras clave (separadas por coma): ").split(',')
    info["otros_datos"]["pelicula_favorita"] = get_input("Película favorita: ")
    info["otros_datos"]["hobby"] = get_input("Hobby o pasatiempo: ")
    info["otros_datos"]["musica"] = get_input("Música o banda favorita: ")
    return info

def generate_base_words(info):
    """Crea una lista de palabras base a partir de la información recolectada."""
    words = set()

    def extract_words(data):
        if isinstance(data, dict):
            for value in data.values():
                extract_words(value)
        elif isinstance(data, list):
            for item in data:
                extract_words(item)
        elif isinstance(data, str) and data:
            # *** CAMBIO CLAVE 1: Eliminación de espacios ***
            # Divide cualquier frase en palabras individuales para evitar espacios.
            for word in data.lower().split():
                words.add(word)
    
    extract_words(info)

    # Extraer iniciales
    def get_initials(nombres, apellidos):
        initials = ""
        for n in nombres:
            if n: initials += n[0]
        for a in apellidos:
            if a: initials += a[0]
        return initials.lower()

    if info["persona_principal"]["nombres"]:
        words.add(get_initials(info["persona_principal"]["nombres"], info["persona_principal"]["apellidos"]))
    for hijo in info["familia"]["hijos"]:
        if hijo["nombres"]:
            words.add(get_initials(hijo["nombres"], hijo["apellidos"]))

    # Extraer partes de fechas
    def extract_date_parts(date_obj):
        if not date_obj: return
        words.add(str(date_obj.day))
        words.add(f"{date_obj.day:02d}")
        words.add(str(date_obj.month))
        words.add(f"{date_obj.month:02d}")
        words.add(str(date_obj.year))
        words.add(str(date_obj.year)[2:])

    extract_date_parts(info["persona_principal"]["fecha_nacimiento"])
    for hijo in info["familia"]["hijos"]:
        extract_date_parts(hijo["fecha_nacimiento"])

    return list(filter(None, words))

def apply_variations(word):
    """Aplica variaciones de mayúsculas/minúsculas y leetspeak a una palabra."""
    variations = set([word, word.upper(), word.capitalize()])
    leet_word = word
    for char, replacements in LEETSPEAK_MAP.items():
        if char in leet_word:
            leet_word = leet_word.replace(char, replacements[0], 1)
    if leet_word != word:
        variations.add(leet_word)
        variations.add(leet_word.capitalize())
    return list(variations)

def generate_passwords(info, base_words):
    """Genera la lista de contraseñas combinando y mutando las palabras base."""
    passwords = set()
    
    for word in base_words:
        for var in apply_variations(word):
            passwords.add(var)

    for w1, w2 in itertools.permutations(base_words, 2):
        for var1 in apply_variations(w1):
            for var2 in apply_variations(w2):
                passwords.add(f"{var1}{var2}")
                passwords.add(f"{var1}{var2}!")
                passwords.add(f"{var1}{var2}$")
                passwords.add(f"{var1}{var2}123")

    # *** CAMBIO CLAVE 2: Lógica avanzada de [Iniciales]+[Año] mejorada ***
    symbols = ['$', '#', '!', '*', '.', '&', '%', '@']
    
    # Patrón: [Iniciales][Año][Símbolo] y [Año][Iniciales][Símbolo] para cada hijo
    for hijo in info["familia"]["hijos"]:
        if hijo["fecha_nacimiento"] and hijo["nombres"]:
            year = str(hijo["fecha_nacimiento"].year)
            year_short = year[2:]
            
            initials = "".join([n[0] for n in hijo["nombres"]] + [a[0] for a in hijo["apellidos"]])
            
            if initials:
                initial_variations = list(set([initials.lower(), initials.upper(), initials.capitalize()]))
                year_variations = [year, year_short]

                for init_var in initial_variations:
                    for year_var in year_variations:
                        # Combinación sin símbolo
                        passwords.add(f"{init_var}{year_var}")
                        passwords.add(f"{year_var}{init_var}")
                        
                        # Combinación con cada símbolo al final
                        for symbol in symbols:
                            passwords.add(f"{init_var}{year_var}{symbol}")
                            passwords.add(f"{year_var}{init_var}{symbol}")
    
    print(f"\n[+] Generadas {len(passwords)} contraseñas únicas.")
    return list(passwords)

def main():
    """Función principal que orquesta todo el proceso."""
    print_presentation()
    info = gather_information()
    
    print("\n[+] Generando palabras base a partir de la información...")
    base_words = generate_base_words(info)
    print(f"Se encontraron {len(base_words)} palabras base.")
    
    print("[+] Generando la lista de contraseñas con combinaciones y mutaciones...")
    password_list = generate_passwords(info, base_words)
    
    output_filename = get_input("\nIntroduce el nombre del archivo para guardar la lista (ej: wordlist.txt): ", allow_empty=False)
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for password in sorted(password_list):
                f.write(password + '\n')
        print(f"\n[SUCCESS] La lista de contraseñas se ha guardado en '{output_filename}'")
    except Exception as e:
        print(f"\n[ERROR] No se pudo guardar el archivo: {e}")

if __name__ == "__main__":
    main()
