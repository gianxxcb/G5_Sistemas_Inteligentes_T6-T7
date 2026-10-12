"""Evaluacion estructurada del problema de optimizacion del caso 05."""

from __future__ import annotations

import itertools
from typing import Any, Iterable

from codigo.configuracion import cargar_datos

DATOS_CASO = cargar_datos()
ACCIONES = tuple({**accion, "id": accion["codigo"]} for accion in DATOS_CASO["acciones"])
PRESUPUESTO_MAXIMO = float(DATOS_CASO["presupuesto_maximo"])


def _normalizar_cromosoma(cromosoma: Iterable[int] | str) -> tuple[int, ...]:
    """Convierte una representacion binaria en una tupla de 8 bits."""
    if isinstance(cromosoma, str):
        cromosoma = tuple(int(bit) for bit in cromosoma.strip())
    cromosoma = tuple(int(bit) for bit in cromosoma)
    if len(cromosoma) != len(ACCIONES):
        raise ValueError(
            f"El cromosoma debe contener exactamente {len(ACCIONES)} genes binarios."
        )
    if any(bit not in (0, 1) for bit in cromosoma):
        raise ValueError("Cada gen debe ser 0 o 1.")
    return cromosoma


def evaluar_cromosoma(cromosoma: Iterable[int] | str) -> dict[str, Any]:
    """Evalua un cromosoma y devuelve costo, beneficio, factibilidad y fitness."""
    cromosoma = _normalizar_cromosoma(cromosoma)

    costo_total = 0.0
    beneficio_total = 0.0
    acciones_elegidas: list[dict[str, Any]] = []

    for indice, gen in enumerate(cromosoma):
        if gen == 1:
            accion = ACCIONES[indice]
            costo_total += float(accion["costo"])
            beneficio_total += float(accion["beneficio"])
            acciones_elegidas.append(accion)

    factible = costo_total <= PRESUPUESTO_MAXIMO
    exceso = max(0.0, costo_total - PRESUPUESTO_MAXIMO)
    penalizacion = 1_000_000.0 * exceso if not factible else 0.0
    fitness = beneficio_total - penalizacion

    return {
        "cromosoma": cromosoma,
        "fitness": float(fitness),
        "fitness_penalizado": float(fitness),
        "costo": float(costo_total),
        "beneficio": float(beneficio_total),
        "factible": factible,
        "exceso": float(exceso),
        "acciones": [accion["codigo"] for accion in acciones_elegidas],
        "acciones_detalle": acciones_elegidas,
    }


def buscar_optimo_exacto(longitud: int | None = None) -> dict[str, Any]:
    """Busca la mejor combinacion mediante recorrido exhaustivo en 2^n complejos."""
    longitud = longitud if longitud is not None else len(ACCIONES)
    evaluaciones = [evaluar_cromosoma(bits) for bits in itertools.product((0, 1), repeat=longitud)]
    mejor = max(
        evaluaciones,
        key=lambda item: (item["fitness"], -item["costo"] if item["factible"] else -float("inf")),
    )
    return {
        "evaluaciones": evaluaciones,
        "optimo": mejor,
        "mejor_cromosoma": mejor["cromosoma"],
        "mejor_fitness": mejor["fitness"],
    }


optimo_exacto = buscar_optimo_exacto
