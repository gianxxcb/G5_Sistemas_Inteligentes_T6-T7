"""Busqueda exhaustiva del optimo exacto para el caso de optimizacion del proyecto."""

from __future__ import annotations

import itertools
from typing import Any

from codigo.algoritmo_genetico.evaluacion import ACCIONES, evaluar_cromosoma


def evaluar_todas_las_combinaciones(longitud: int | None = None) -> list[dict[str, Any]]:
    """Evalua todas las combinaciones binarias posibles para la cantidad de acciones."""
    longitud = longitud if longitud is not None else len(ACCIONES)
    return [evaluar_cromosoma(bits) for bits in itertools.product((0, 1), repeat=longitud)]


def buscar_optimo_exacto(longitud: int | None = None) -> dict[str, Any]:
    """Devuelve el cromosoma, la evaluacion y el mejor fitness exacto de todas las combinaciones."""
    evaluaciones = evaluar_todas_las_combinaciones(longitud)
    mejor = max(
        evaluaciones,
        key=lambda item: (item["fitness"], -item["costo"] if item["factible"] else float("-inf")),
    )
    return {
        "total_combinaciones": len(evaluaciones),
        "optimo": mejor,
        "mejor_cromosoma": mejor["cromosoma"],
        "mejor_fitness": mejor["fitness"],
        "evaluaciones": evaluaciones,
    }


optimo_exacto = buscar_optimo_exacto
resolver_optimo_exacto = buscar_optimo_exacto
