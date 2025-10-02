Markdown
# Cerbero - Generador de Wordlists Contextuales

```
 _   _  _   _  ____   _   _   ____  
██████╗ ███████╗██████╗ ██████╗ ███████╗ ██████╗  ██████╗ 
██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔═══██╗
██║      █████╗  ██████╔╝██████╔╝█████╗  ██║   ██║██║   ██║
██║      ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██║   ██║██║   ██║
╚██████╗ ███████╗██║  ██║██████╔╝███████╗╚██████╔╝╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ 
  --- Professional Audit Edition v2.2 ---

Cerbero es una suite de herramientas en Python diseñada para el perfilado de credenciales. Su objetivo es generar listas de nombres de usuario y contraseñas altamente personalizadas y eficientes, basadas en información específica de un objetivo. A diferencia de generadores genéricos, Cerbero utiliza datos contextuales para simular los patrones que las personas reales usan para crear sus credenciales, aumentando drásticamente la efectividad en auditorías de seguridad y pentesting ético.

¿Por qué Cerbero?
Las herramientas estándar de generación de wordlists a menudo fallan al intentar adivinar credenciales basadas en la vida personal de un usuario. Es un hecho conocido que una gran cantidad de personas crean contraseñas y nombres de usuario usando una mezcla de:
Nombres, apellidos y sus iniciales.
Nombres de hijos, parejas o mascotas.
Fechas de nacimiento o aniversarios.
Apodos, hobbies o frases favoritas.

Cerbero fue creado para explotar estos patrones, aplicando lógica avanzada y mutaciones inteligentes a un conjunto de datos personales para construir listas de credenciales mucho más efectivas que las genéricas.

Características Principales
Suite de Herramientas Integrada: Un único script con un menú interactivo para acceder a todas las funcionalidades.

Múltiples Modos de Operación:
Generador de Contraseñas Completo: Crea contraseñas complejas mezclando letras, números y símbolos a partir de un cuestionario exhaustivo.

Generador de Nombres de Usuario: Crea listas de usuarios potenciales basados en patrones comunes (d.ugalde, dugalde81, daniel.ugalde, etc.).

Generador de PINs Numéricos: Especializado en la creación de códigos numéricos para auditorías específicas.

Modo de Auditoría: Permite a un usuario verificar si su propia contraseña se encuentra en una de las listas generadas, promoviendo la seguridad defensiva.

Lógica de Generación Avanzada: Implementa patrones de contraseñas modernos y comunes como [AñoActual][NombreEnLeetSpeak][Símbolo].

Mutaciones Inteligentes: Aplica automáticamente variaciones de mayúsculas/minúsculas (test, Test, TEST) y transformaciones Leetspeak (daniel -> d4n13l).

Filtros de Eficiencia: Permite establecer una longitud mínima y máxima para las contraseñas, optimizando el tamaño de la wordlist y el tiempo de auditoría.

Código Abierto y sin Dependencias: Escrito en Python puro, fácil de entender, modificar y ejecutar en cualquier sistema.
Instalación
Cerbero no requiere instalación compleja.
Requisitos:
Python 3.6 o superior.
Pasos:
Clona el repositorio en tu máquina local:

Bash
git clone https://github.com/syruxst/cerbero.git
Navega al directorio del proyecto:

Bash
cd cerbero
¡Y eso es todo! Ya estás listo para usar la herramienta.
Modo de Uso
Ejecuta el script desde tu terminal para acceder al menú principal.

Bash
python cerberoV2-3.py

Aparecerá un menú con las siguientes opciones:

1. Modo Completo (Generar Wordlist de Contraseñas)
Inicia un cuestionario detallado para recopilar información sobre el objetivo. Al finalizar, genera miles de contraseñas candidatas y las filtra por longitud antes de guardarlas.
2. Modo Numérico (Generar PINs / Códigos)
Diseñado para auditar sistemas con contraseñas exclusivamente numéricas. Pide datos numéricos (fechas, RUT, etc.) y genera combinaciones dentro de un rango de longitud.
3. Modo Nombres de Usuario (Generar Userlist)
Pide información básica (nombres, apellidos, apodo) y genera una lista de nombres de usuario potenciales siguiendo patrones corporativos y de plataformas web comunes.
4. Modo Auditoría (Buscar tu contraseña o usuario en una lista)
Una herramienta defensiva. Te pide la ruta a una wordlist y una contraseña, y te informa si esa contraseña existe en la lista, ayudándote a evaluar su seguridad.
5. Salir
Termina la ejecución del programa.
El programa volverá al menú principal después de cada acción (excepto "Salir") para un flujo de trabajo continuo.

Advertencia de Uso Ético
[!] IMPORTANTE: Cerbero es una herramienta creada con fines educativos y para ser utilizada exclusivamente en auditorías de seguridad y pentesting dentro de un marco legal y con autorización explícita del propietario del sistema. El uso no autorizado de esta herramienta para intentar acceder a sistemas ajenos es ilegal. El autor no se hace responsable del mal uso de este programa.
Cómo Contribuir
¡Las contribuciones son bienvenidas! Si tienes ideas para nuevas reglas de generación, optimizaciones o correcciones, no dudes en participar.
Haz un "Fork" del proyecto.
Crea una nueva rama para tu funcionalidad (git checkout -b feature/AmazingFeature).
Haz "Commit" de tus cambios (git commit -m 'Add some AmazingFeature').
Haz "Push" a la rama (git push origin feature/AmazingFeature).
Abre un "Pull Request".
Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
Autor
Daniel Ugalde - https://github.com/syruxst/cerbero
