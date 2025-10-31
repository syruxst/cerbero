# De Cero a Hacker con Python: Desmontando Cerbero

¡Bienvenido/a a la guía definitiva para entender y modificar Cerbero! Si alguna vez has querido aprender Python creando una herramienta de ciberseguridad real, estás en el lugar correcto. No necesitas experiencia previa en programación, solo curiosidad y ganas de aprender.

Esta guía te llevará de la mano a través del código de Cerbero, explicando cada pieza como si fuera un bloque de LEGO. Al final, no solo entenderás cómo funciona la herramienta, sino que también tendrás las habilidades para modificarla y crear tus propias lógicas de ataque.

---

## Capítulo 1: Los Cimientos del Código (Conceptos Básicos de Python)

Todo gran edificio necesita cimientos sólidos. En programación, esos cimientos son las variables, las funciones y las estructuras de control. Vamos a ver cómo Cerbero los utiliza.

### 1.1. Variables: Las "Cajas" para Guardar Información

Piensa en una variable como una caja con una etiqueta. Puedes guardar cualquier cosa dentro (un texto, un número) y luego referirte a ella por su etiqueta.

En Cerbero, usamos variables para todo. Por ejemplo, al principio del código, vemos esto:

```python
BANNER = f"""{Colors.MAGENTA}
██████╗ ...
{Colors.RESET}"""

LEETSPEAK_MAP = {'a': ['4', '@'], 'e': ['3'], ...}
BANNER: Es una "caja" (variable) que contiene el logo gigante en arte ASCII. 
En lugar de escribir el logo cada vez que lo necesitamos, simplemente llamamos a la caja BANNER.
LEETSPEAK_MAP: Es una caja especial llamada diccionario. 
Funciona como un diccionario real: tienes una "palabra" (la clave, ej: 'a') y su "definición" (el valor, ej: ['4', '@']). Así, podemos buscar fácilmente las sustituciones para cada letra.
```
### 2. Funciones: "Mini-Programas" Reutilizables
Una función es como una receta de cocina. Es un conjunto de instrucciones que 
realiza una tarea específica. En lugar de escribir los mismos pasos una y otra vez, 
simplemente "llamas a la receta" por su nombre. En Python, se definen con def.
Veamos una de las funciones más importantes de Cerbero, get_input:

```python
def get_input(prompt, allow_empty=True, normalize=False):
    full_prompt = f"{Colors.BLUE}{prompt}{Colors.RESET}"
    while True:
        value = input(full_prompt).strip()
        if value or allow_empty: 
            return normalize_string(value) if normalize and value else value
        print(f"{Colors.YELLOW}Este campo no puede estar vacío.{Colors.RESET}")
```
## Desmontemos esta "receta":

def get_input(...): Define una función llamada get_input. Los elementos entre paréntesis son los "ingredientes" que necesita la receta para funcionar. prompt es el texto de la pregunta que queremos hacer.
while True:: Esto crea un bucle infinito. Es como decir "sigue haciendo esto para siempre... hasta que te diga que pares".
value = input(full_prompt).strip(): Esta es la instrucción clave. input() es una función de Python que muestra un mensaje en la pantalla y espera a que el usuario escriba algo y presione Enter. .strip() es un truco que elimina espacios en blanco al principio y al final, ¡muy útil para limpiar la entrada!
if value or allow_empty:: Esto es una condición. Es como preguntar "¿el usuario escribió algo, o le permitimos dejarlo en blanco?".
return ...: Esta es la instrucción para "parar" el bucle y devolver el resultado. La receta ha terminado y nos entrega el plato final (el texto que el usuario escribió).
Si la condición if no se cumple (el usuario no escribió nada y no estaba permitido), el bucle continúa y vuelve a pedir la información.
1.3. Clases: El "Molde" para Crear Objetos
Una clase es como el plano o molde para crear algo. En Cerbero, usamos una clase muy simple pero poderosa para manejar los colores:

```python
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    # ... y así sucesivamente
```