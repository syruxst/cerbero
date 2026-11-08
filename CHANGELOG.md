# Changelog

Todas las novedades relevantes de Cerbero se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [8.0.0] - 2026-11-07

### Añadido
- **Paquete instalable** (`pyproject.toml`): `pip install .` crea el comando
  `cerbero`. Instalación recomendada con `pipx`.
- **CLI con subcomandos**: `generate`, `audit`, `merge`, `init-profile`, además
  del menú interactivo por defecto.
- **Modo headless real** mediante perfiles de objetivo YAML/JSON
  (`cerbero generate --config perfil.yaml`). Antes `full/numeric/username`
  headless solo imprimían un aviso.
- **`cerbero init-profile`**: genera un perfil de ejemplo comentado.
- **Modo `--stdout`**: emite las contraseñas por stdout para encadenar con
  hashcat/john (`cerbero generate ... --stdout | hashcat ...`). El diagnóstico
  va por stderr para no contaminar la wordlist.
- **Interfaz Rich** (tablas, paneles, reglas) con degradación elegante a ANSI
  si `rich` no está instalado.
- **Logging** configurable (`-v`, `-vv`) centralizado en el logger `cerbero`.
- **Pipeline de generación único** (`cerbero.core.pipeline`) compartido por los
  modos interactivo y headless.
- **Suite de tests ampliada** (perfiles, pipeline, CLI) y configuración de
  `ruff` + `mypy` + CI (GitHub Actions) en Python 3.9–3.12.
- Marcador `py.typed` (PEP 561).

### Corregido
- **Validador de fortaleza**: el orden de las ramas `elif` dejaba inalcanzables
  los bonos de longitud `>=16` y de entropía `>80`.
- **Límite global**: el tope `--limit` se aplicaba por motor y podía
  multiplicarse por 12; ahora es un tope global real.
- **Motor 5**: iteraba un `set`, produciendo wordlists no reproducibles entre
  ejecuciones; ahora es determinista.

### Cambiado
- Reestructuración a un único paquete `cerbero/` (antes módulos sueltos en la
  raíz).
- `__pycache__`/`.pyc` y backups retirados del control de versiones
  (`.gitignore`).

[8.0.0]: https://github.com/syruxst/cerbero/releases/tag/v8.0.0
