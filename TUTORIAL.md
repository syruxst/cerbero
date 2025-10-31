Guía Completa: "De Cero a Hacker con Python: Desmontando Cerbero"
De Cero a Hacker con Python: Desmontando Cerbero
¡Bienvenido/a a la guía definitiva para entender y modificar Cerbero! Si alguna vez has querido aprender Python creando una herramienta de ciberseguridad real, estás en el lugar correcto. No necesitas experiencia previa en programación, solo curiosidad y ganas de aprender.
Esta guía te llevará de la mano a través del código de Cerbero, explicando cada pieza como si fuera un bloque de LEGO. Al final, no solo entenderás cómo funciona la herramienta, sino que también tendrás las habilidades para modificarla y crear tus propias lógicas de ataque.
Capítulo 1: Los Cimientos del Código (Conceptos Básicos de Python)
Todo gran edificio necesita cimientos sólidos. En programación, esos cimientos son las variables, las funciones y las estructuras de control. Vamos a ver cómo Cerbero los utiliza.
1.1. Variables: Las "Cajas" para Guardar Información
Piensa en una variable como una caja con una etiqueta. Puedes guardar cualquier cosa dentro (un texto, un número) y luego referirte a ella por su etiqueta.
En Cerbero, usamos variables para todo. Por ejemplo, al principio del código, vemos esto:
code
Python
BANNER = f"""{Colors.MAGENTA}
██████╗ ...
{Colors.RESET}"""

LEETSPEAK_MAP = {'a': ['4', '@'], 'e': ['3'], ...}
BANNER: Es una "caja" (variable) que contiene el logo gigante en arte ASCII. En lugar de escribir el logo cada vez que lo necesitamos, simplemente llamamos a la caja BANNER.
LEETSPEAK_MAP: Es una caja especial llamada diccionario. Funciona como un diccionario real: tienes una "palabra" (la clave, ej: 'a') y su "definición" (el valor, ej: ['4', '@']). Así, podemos buscar fácilmente las sustituciones para cada letra.
1.2. Funciones: "Mini-Programas" Reutilizables
Una función es como una receta de cocina. Es un conjunto de instrucciones que realiza una tarea específica. En lugar de escribir los mismos pasos una y otra vez, simplemente "llamas a la receta" por su nombre. En Python, se definen con def.
Veamos una de las funciones más importantes de Cerbero, get_input:
code
Python
def get_input(prompt, allow_empty=True, normalize=False):
    full_prompt = f"{Colors.BLUE}{prompt}{Colors.RESET}"
    while True:
        value = input(full_prompt).strip()
        if value or allow_empty: 
            return normalize_string(value) if normalize and value else value
        print(f"{Colors.YELLOW}Este campo no puede estar vacío.{Colors.RESET}")
Desmontemos esta "receta":
def get_input(...): Define una función llamada get_input. Los elementos entre paréntesis son los "ingredientes" que necesita la receta para funcionar. prompt es el texto de la pregunta que queremos hacer.
while True:: Esto crea un bucle infinito. Es como decir "sigue haciendo esto para siempre... hasta que te diga que pares".
value = input(full_prompt).strip(): Esta es la instrucción clave. input() es una función de Python que muestra un mensaje en la pantalla y espera a que el usuario escriba algo y presione Enter. .strip() es un truco que elimina espacios en blanco al principio y al final, ¡muy útil para limpiar la entrada!
if value or allow_empty:: Esto es una condición. Es como preguntar "¿el usuario escribió algo, o le permitimos dejarlo en blanco?".
return ...: Esta es la instrucción para "parar" el bucle y devolver el resultado. La receta ha terminado y nos entrega el plato final (el texto que el usuario escribió).
Si la condición if no se cumple (el usuario no escribió nada y no estaba permitido), el bucle continúa y vuelve a pedir la información.
1.3. Clases: El "Molde" para Crear Objetos
Una clase es como el plano o molde para crear algo. En Cerbero, usamos una clase muy simple pero poderosa para manejar los colores:
code
Python
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    # ... y así sucesivamente
class Colors:: Define un "molde" llamado Colors.
Dentro del molde, hemos creado variables (RESET, RED, etc.) que contienen códigos especiales que las terminales entienden como colores.
¿Por qué usar una clase? Para organizar. Ahora, cada vez que queremos usar el color rojo, no tenemos que recordar el código \033[91m. Simplemente escribimos Colors.RED. Es mucho más limpio y fácil de leer.
Capítulo 2: El Corazón de Cerbero - Los Motores de Generación
Aquí es donde ocurre la magia. Cerbero no tiene una, sino ocho lógicas de ataque diferentes, cada una encapsulada en su propia función "motor". Vamos a analizar dos de los más interesantes.
2.1. Anatomía de un Motor: motor_4_centrado_en_hijos
Este motor implementa la lógica AñoHijo + InicialesHijo + Símbolo.
code
Python
def motor_4_centrado_en_hijos(info, text_words, numeric_words, symbols, add_func):
    count = 0
    # 1. Recorrer la lista de hijos que el usuario introdujo
    for hijo in info.get("familia", {}).get("hijos", []):
        # 2. Verificar si tenemos los datos necesarios (fecha y nombre)
        if hijo.get("fecha_nacimiento") and hijo.get("nombres"):
            # 3. Extraer y formatear los datos
            year = str(hijo["fecha_nacimiento"].year)
            initials = "".join([n[0] for n in hijo["nombres"] if n] + [a[0] for a in hijo.get("apellidos", []) if a]).lower()
            
            if initials:
                initials_cased = initials.capitalize()
                # 4. Generar todas las combinaciones y añadirlas
                for sym in symbols:
                    count += add_func(f"{year}{initials_cased}{sym}")      # ej: 2014Jiub$
                    count += add_func(f"{initials_cased}{year}{sym}")      # ej: Jiub2014$
                    count += add_func(f"{initials_cased}{sym}{year}")      # ej: Jiub$2014
    return count
Puntos clave para modificar:
¿Quieres añadir el año corto? Simplemente añade year_short = year[2:] y úsalo en las combinaciones.
¿Quieres probar con todas las iniciales en mayúsculas? Añade initials_upper = initials.upper() y genera más contraseñas con él.
¿Quieres añadir el día de nacimiento? Extráelo de hijo["fecha_nacimiento"].day y añádelo a las combinaciones.
2.2. El "Jefe Final": motor_8_cadenas_biograficas
Este es el motor más complejo y potente. Implementa la lógica S76b96j14.
code
Python
def motor_8_cadenas_biograficas(info, text_words, numeric_words, symbols, add_func):
    count = 0
    people = [] # 1. Lista para guardar los "pares biográficos"

    # 2. Recolectar los datos de la pareja e hijos
    pareja = info.get("familia", {}).get("pareja", {})
    if pareja.get("nombres") and pareja.get("fecha_nacimiento"):
        people.append({"initial": pareja["nombres"][0][0], "year_short": str(pareja["fecha_nacimiento"].year)[2:]})
    
    for hijo in info.get("familia", {}).get("hijos", []):
        if hijo.get("nombres") and hijo.get("fecha_nacimiento"):
            people.append({"initial": hijo["nombres"][0][0], "year_short": str(hijo["fecha_nacimiento"].year)[2:]})

    if len(people) < 2: # 3. Salir si no hay suficientes datos
        # ...
        return 0
        
    # 4. Generar permutaciones del ORDEN de las personas
    for length in range(2, len(people) + 1):
        for p_people in itertools.permutations(people, length):
            
            # 5. Para cada orden, preparar las variaciones de CADA eslabón
            chunk_variations_for_permutation = []
            for person in p_people:
                initial_lower = person['initial'].lower(); initial_upper = person['initial'].upper(); year = person['year_short']
                # Cada eslabón tiene dos posibles variaciones: s76 y S76
                chunk_variations_for_permutation.append([f"{initial_lower}{year}", f"{initial_upper}{year}"])
            
            # 6. La magia: itertools.product crea TODAS las combinaciones posibles
            for combo in itertools.product(*chunk_variations_for_permutation):
                count += add_func("".join(combo))
    return count
Este motor utiliza itertools, una de las librerías más poderosas de Python para crear combinaciones y permutaciones complejas. Entenderlo es entender el corazón de la generación de contraseñas avanzadas.
Capítulo 3: El Cerebro Organizador - run_full_mode y la Lógica Principal
Tener muchos motores es genial, pero necesitas un "director de orquesta" que decida cuándo y cómo se ejecutan. Esa es la función run_full_mode.
3.1. El Cuestionario Inteligente
Al principio de run_full_mode, verás este bloque:
code
Python
engine_dependencies = {'1': ['principal', ...], '8': ['pareja', 'hijos']}
    # ...
    engines_to_run = [e.strip() for e in engines_input.lower().split(',')]
    
    required_sections = set()
    if 'all' in engines_to_run: 
        required_sections = {'principal', 'pareja', 'hijos', 'otros', 'mangle', 'familia'}
    else:
        for eng in engines_to_run:
            if eng in engine_dependencies:
                required_sections.update(engine_dependencies[eng])
    
    info = gather_smart_information(required_sections)
engine_dependencies: Es un diccionario que mapea cada motor a los "tipos de datos" que necesita. El Motor 8, por ejemplo, solo necesita datos de pareja e hijos.
El código revisa qué motores seleccionaste y construye una lista (required_sections) de todos los tipos de datos únicos que se necesitarán.
Finalmente, llama a gather_smart_information y le pasa esa lista, para que solo haga las preguntas relevantes.
3.2. El Bucle Principal y el Manejo de Ctrl+C
La función main es el punto de entrada de todo el programa. Observa su estructura:
code
Python
def main():
    print_presentation()
    try:
        while True:
            # 1. Muestra el menú y pide una opción
            # ...
            if choice == '1': run_full_mode()
            # ...
            elif choice == '5': break # Solo 'Salir' rompe el bucle
            # ...
    except KeyboardInterrupt:
        # 2. Si se presiona Ctrl+C en cualquier momento...
        print("\n\n[INFO] Salida solicitada por el usuario...")
        sys.exit(0) # ...el programa sale de forma limpia.
Esta estructura try...except es un pilar de la programación robusta en Python. Permite que tu programa maneje errores inesperados (o interrupciones del usuario) con elegancia, en lugar de simplemente "romperse".
¡Ahora es tu turno!
Has visto los cimientos, la lógica de los motores y la estructura principal. Ahora tienes el conocimiento para empezar a experimentar.
Ideas para empezar a modificar:
Añade un Símbolo a un Motor: Ve al motor_1_combinaciones_simples y añade + symbols[0] al final de una de las combinaciones. ¡Acabas de añadir una nueva regla!
Crea un Nuevo Motor (Motor 9): Copia y pega el motor_1, renómbralo a motor_9_mi_logica, y modifica las combinaciones para que haga algo nuevo. ¡No olvides añadirlo a la lista engine_functions!
Cambia los Colores: Ve a la clase Colors al principio y cambia el código de Colors.GREEN por el de Colors.CYAN (\033[96m). ¡Acabas de personalizar la interfaz!
El código abierto es una invitación a explorar, aprender y construir. Cerbero es ahora tu laboratorio. ¡Diviértete y construir. Cerbero es ahora tu laboratorio. ¡Diviértete!

