"""
Cerbero - Consola compartida.

Envoltorio sobre `rich` con degradación elegante: si `rich` no está
instalado, cae a `print` con códigos ANSI. Todo el resto del código usa
estos helpers en lugar de `print` directo para una UI consistente.
"""
from __future__ import annotations

import sys
from typing import Any, Optional

from .utils import Colors

try:
    from rich.console import Console as _RichConsole
    from rich.theme import Theme

    _THEME = Theme(
        {
            "info": "cyan",
            "ok": "bold green",
            "warn": "yellow",
            "err": "bold red",
            "accent": "magenta",
            "muted": "dim",
        }
    )
    RICH_AVAILABLE = True
except Exception:  # pragma: no cover - rich siempre presente en entorno soportado
    RICH_AVAILABLE = False
    _RichConsole = None  # type: ignore[assignment,misc]
    _THEME = None  # type: ignore[assignment]


class ConsoleProxy:
    """Fachada de salida. Usa rich si está disponible; si no, ANSI plano."""

    def __init__(self, *, stderr: bool = False, no_color: bool = False) -> None:
        self._stderr = stderr
        self._stream = sys.stderr if stderr else sys.stdout
        self.no_color = no_color
        if RICH_AVAILABLE and not no_color:
            self._rich: Optional[Any] = _RichConsole(theme=_THEME, stderr=stderr)
        else:
            self._rich = None

    @property
    def rich(self) -> Optional[Any]:
        """Consola rich subyacente (o None en modo fallback)."""
        return self._rich

    def print(self, *args: Any, **kwargs: Any) -> None:
        if self._rich is not None:
            self._rich.print(*args, **kwargs)
        else:
            # Quitar estilos tipo rich "[info]...[/info]" en fallback simple.
            text = " ".join(str(a) for a in args)
            self._stream.write(text + "\n")

    # --- Helpers semánticos (siempre funcionan, con o sin rich) -----------
    def info(self, msg: str) -> None:
        if self._rich is not None:
            self._rich.print(f"[info][*][/info] {msg}")
        else:
            self._stream.write(f"{Colors.CYAN}[*]{Colors.RESET} {msg}\n")

    def ok(self, msg: str) -> None:
        if self._rich is not None:
            self._rich.print(f"[ok][+][/ok] {msg}")
        else:
            self._stream.write(f"{Colors.GREEN}[+]{Colors.RESET} {msg}\n")

    def warn(self, msg: str) -> None:
        if self._rich is not None:
            self._rich.print(f"[warn][!][/warn] {msg}")
        else:
            self._stream.write(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}\n")

    def error(self, msg: str) -> None:
        if self._rich is not None:
            self._rich.print(f"[err][x][/err] {msg}")
        else:
            self._stream.write(f"{Colors.RED}[x]{Colors.RESET} {msg}\n")

    def rule(self, title: str = "") -> None:
        if self._rich is not None:
            self._rich.rule(title)
        else:
            self._stream.write(f"\n{'=' * 70}\n{title}\n{'=' * 70}\n")


# Consola global de la aplicación (salida a stdout).
console = ConsoleProxy()
# Consola de diagnóstico (stderr) — para no contaminar wordlists en modo --stdout.
err_console = ConsoleProxy(stderr=True)
