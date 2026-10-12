"""Base explicita de reglas para la urgencia de recoleccion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReglaDifusa:
    """Regla SI-ENTONCES con tres antecedentes y una consecuencia."""

    codigo: str
    llenado: str
    tiempo: str
    afluencia: str
    urgencia: str


def crear_reglas_urgencia() -> tuple[ReglaDifusa, ...]:
    """Devuelve reglas coherentes que cubren las 27 combinaciones linguisticas."""
    return (
        ReglaDifusa("RD01", "bajo", "corto", "baja", "baja"),
        ReglaDifusa("RD02", "bajo", "corto", "media", "baja"),
        ReglaDifusa("RD03", "bajo", "corto", "alta", "media"),
        ReglaDifusa("RD04", "bajo", "medio", "baja", "baja"),
        ReglaDifusa("RD05", "bajo", "medio", "media", "media"),
        ReglaDifusa("RD06", "bajo", "medio", "alta", "alta"),
        ReglaDifusa("RD07", "bajo", "largo", "baja", "media"),
        ReglaDifusa("RD08", "bajo", "largo", "media", "alta"),
        ReglaDifusa("RD09", "bajo", "largo", "alta", "alta"),
        ReglaDifusa("RD10", "medio", "corto", "baja", "baja"),
        ReglaDifusa("RD11", "medio", "corto", "media", "media"),
        ReglaDifusa("RD12", "medio", "corto", "alta", "media"),
        ReglaDifusa("RD13", "medio", "medio", "baja", "media"),
        ReglaDifusa("RD14", "medio", "medio", "media", "media"),
        ReglaDifusa("RD15", "medio", "medio", "alta", "alta"),
        ReglaDifusa("RD16", "medio", "largo", "baja", "media"),
        ReglaDifusa("RD17", "medio", "largo", "media", "alta"),
        ReglaDifusa("RD18", "medio", "largo", "alta", "alta"),
        ReglaDifusa("RD19", "alto", "corto", "baja", "media"),
        ReglaDifusa("RD20", "alto", "corto", "media", "alta"),
        ReglaDifusa("RD21", "alto", "corto", "alta", "alta"),
        ReglaDifusa("RD22", "alto", "medio", "baja", "alta"),
        ReglaDifusa("RD23", "alto", "medio", "media", "alta"),
        ReglaDifusa("RD24", "alto", "medio", "alta", "alta"),
        ReglaDifusa("RD25", "alto", "largo", "baja", "alta"),
        ReglaDifusa("RD26", "alto", "largo", "media", "alta"),
        ReglaDifusa("RD27", "alto", "largo", "alta", "alta"),
    )
