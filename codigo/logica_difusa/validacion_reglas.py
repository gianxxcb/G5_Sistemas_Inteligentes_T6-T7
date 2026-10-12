"""Validacion de cobertura, consistencia y casos de prueba del sistema difuso."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from codigo.logica_difusa.casos_prueba import ejecutar_casos_prueba
from codigo.logica_difusa.reglas import crear_reglas_urgencia


def validar_reglas_urgencia(reglas: tuple[Any, ...] | None = None) -> dict[str, Any]:
    """Comprueba cobertura completa y posibles contradicciones entre reglas."""
    reglas = tuple(reglas) if reglas is not None else crear_reglas_urgencia()
    combinaciones: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    contradicciones: list[dict[str, Any]] = []

    for regla in reglas:
        clave = (regla.llenado, regla.tiempo, regla.afluencia)
        combinaciones[clave].append(regla.urgencia)

    faltantes: list[tuple[str, str, str]] = []
    for llenado in ("bajo", "medio", "alto"):
        for tiempo in ("corto", "medio", "largo"):
            for afluencia in ("baja", "media", "alta"):
                clave = (llenado, tiempo, afluencia)
                if clave not in combinaciones:
                    faltantes.append(clave)
                elif len(set(combinaciones[clave])) > 1:
                    contradicciones.append(
                        {
                            "antecedentes": {"llenado": llenado, "tiempo": tiempo, "afluencia": afluencia},
                            "consecuencias": combinaciones[clave],
                        }
                    )

    return {
        "total_reglas": len(reglas),
        "cobertura_completa": not faltantes and not contradicciones,
        "faltantes": faltantes,
        "contradicciones": contradicciones,
        "casos": ejecutar_casos_prueba(),
    }


def validar_cobertura_reglas() -> dict[str, Any]:
    """Alias para la validacion de cobertura del motor difuso."""
    return validar_reglas_urgencia()


analizar_reglas_urgencia = validar_reglas_urgencia
