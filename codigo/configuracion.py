"""Datos compartidos y parametros del caso 05."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_PROYECTO / "datos" / "caso_05.json"

DEFINICIONES_PERTENENCIA: dict[str, dict[str, tuple[str, tuple[float, ...]]]] = {
    "llenado": {
        "bajo": ("trapezoidal", (0.0, 0.0, 25.0, 45.0)),
        "medio": ("triangular", (30.0, 50.0, 70.0)),
        "alto": ("trapezoidal", (55.0, 75.0, 100.0, 100.0)),
    },
    "tiempo": {
        "corto": ("trapezoidal", (0.0, 0.0, 2.0, 4.0)),
        "medio": ("triangular", (3.0, 5.0, 7.0)),
        "largo": ("trapezoidal", (6.0, 8.0, 10.0, 10.0)),
    },
    "afluencia": {
        "baja": ("trapezoidal", (0.0, 0.0, 25.0, 45.0)),
        "media": ("triangular", (30.0, 50.0, 70.0)),
        "alta": ("trapezoidal", (55.0, 75.0, 100.0, 100.0)),
    },
    "urgencia": {
        "baja": ("trapezoidal", (0.0, 0.0, 25.0, 45.0)),
        "media": ("triangular", (30.0, 50.0, 70.0)),
        "alta": ("trapezoidal", (55.0, 75.0, 100.0, 100.0)),
    },
}

LIMITES_VARIABLES: dict[str, tuple[float, float]] = {
    "llenado": (0.0, 100.0),
    "tiempo": (0.0, 10.0),
    "afluencia": (0.0, 100.0),
    "urgencia": (0.0, 100.0),
}


def cargar_datos() -> dict[str, Any]:
    """Carga los datos del caso desde el archivo JSON del proyecto."""
    with RUTA_DATOS.open(encoding="utf-8") as archivo:
        return json.load(archivo)
