Markdown
# Cerbero - Generador de Wordlists Contextuales

```ascii
 _   _  _   _  ____   _   _   ____  
██████╗ ███████╗██████╗ ██████╗ ███████╗ ██████╗  ██████╗ 
██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔═══██╗
██║      █████╗  ██████╔╝██████╔╝█████╗  ██║   ██║██║   ██║
██║      ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██║   ██║██║   ██║
╚██████╗ ███████╗██║  ██║██████╔╝███████╗╚██████╔╝╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ 
  --- Professional Audit Edition v2.2 ---

Cerbero es una herramienta de línea de comandos en Python diseñada para generar wordlists (listas de contraseñas) altamente personalizadas y eficientes, basadas en información específica de un objetivo. A diferencia de generadores genéricos, Cerbero utiliza datos contextuales para crear contraseñas que las personas realmente usan, aumentando drásticamente la efectividad en auditorías de seguridad y pentesting ético.

¿Por qué Cerbero?

Las herramientas estándar de generación de wordlists son potentes para crear combinaciones alfanuméricas, pero fallan al intentar adivinar contraseñas basadas en la vida personal de un usuario. Es un hecho conocido que una gran cantidad de personas crean contraseñas usando una mezcla de:
Nombres de hijos, parejas o mascotas.
Fechas de nacimiento o aniversarios.
Apodos, hobbies o frases favoritas.
Cerbero fue creado para llenar este vacío, aplicando lógica avanzada y mutaciones inteligentes a un conjunto de datos personales para simular los patrones de creación de contraseñas humanas.
Características Principales
Generación Contextual: Crea contraseñas a partir de nombres, apellidos, fechas, apodos, hobbies y más.
Múltiples Modos de Operación:
Modo Completo: Genera contraseñas complejas mezclando letras, números y símbolos.
Modo Numérico: Especializado en la creación de PINs y códigos numéricos para auditorías específicas.
Lógica Avanzada: Implementa patrones comunes como [Año][Iniciales][Símbolo] o [Mascota][Número].
Mutaciones Inteligentes: Aplica automáticamente variaciones de mayúsculas/minúsculas (test, Test, TEST) y transformaciones Leetspeak (test -> t3st, T3ST).
Filtros de Eficiencia: Permite establecer una longitud mínima y máxima para las contraseñas, optimizando el tamaño de la wordlist y el tiempo de auditoría.
Interfaz Interactiva: Guía al usuario a través de un cuestionario para recopilar la información de forma sencilla.
Código Abierto: Escrito en Python sin dependencias externas, fácil de entender y modificar.
Instalación
Cerbero es un script de Python y no requiere instalación compleja ni dependencias externas.
Requisitos:
Python 3.6 o superior.
Pasos:
Clona el repositorio en tu máquina local:

Bash
git clone https://github.com/tu-usuario/Cerbero.git
Navega al directorio del proyecto:

Bash
cd Cerbero
¡Y eso es todo! Ya estás listo para usar la herramienta.
Modo de Uso
Ejecuta el script desde tu terminal. Aparecerá un menú para que elijas el modo de operación.

Bash
python cerberoV2-2.py

Modo 1: Completo (Wordlist Avanzada)
Esta opción inicia un cuestionario detallado para recopilar la mayor cantidad de información posible sobre el objetivo.
Responde a las preguntas sobre el objetivo, su familia, mascotas, hobbies, etc. (Puedes dejar en blanco las que no sepas).
Al finalizar, el programa te pedirá definir una longitud mínima y máxima para las contraseñas.
Cerbero generará miles de combinaciones, las filtrará según el rango de longitud y las guardará en el archivo que especifiques.

Modo 2: Numérico (PINs / Códigos)
Este modo está diseñado para auditar sistemas que usan contraseñas exclusivamente numéricas (PINs de 4 dígitos, claves de acceso basadas en RUT, etc.).

Responde a las preguntas enfocadas en datos numéricos (RUT, fechas, números de teléfono, etc.).
Define un rango de longitud para los códigos a generar (ej. de 4 a 8 dígitos).
La herramienta creará permutaciones de los datos numéricos y guardará el resultado en un archivo.

Advertencia de Uso Ético

[!] IMPORTANTE: Cerbero es una herramienta creada con fines educativos y para ser utilizada exclusivamente en auditorías de seguridad y pentesting dentro de un marco legal y con autorización explícita del propietario del sistema. El uso no autorizado de esta herramienta para intentar acceder a sistemas ajenos es ilegal. El autor no se hace responsable del mal uso de este programa.

Cómo Contribuir
¡Las contribuciones son bienvenidas! Si tienes ideas para nuevas reglas de generación, optimizaciones o correcciones, no dudes en participar.

Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
Autor
Daniel Ugalde - https://github.com/syruxst# cerbero
