"""Casos de prueba y tablas de salida para la validacion del motor difuso."""

from __future__ import annotations

from typing import Any, Iterable

from codigo.configuracion import cargar_datos
from codigo.logica_difusa.inferencia_mamdani import evaluar_urgencia


CASOS_BASE = tuple(cargar_datos()["registros_prueba"])
CASOS_ADICIONALES = (
    {"identificador": "N01", "llenado": 10, "tiempo": 9, "afluencia": 20},
    {"identificador": "N02", "llenado": 60, "tiempo": 5, "afluencia": 70},
)


def ejecutar_casos_prueba(casos: Iterable[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Ejecuta la logica difusa para una lista de casos y devuelve la tabla resultante."""
    casos = tuple(casos if casos is not None else CASOS_BASE + CASOS_ADICIONALES)
    resultados: list[dict[str, Any]] = []
    for caso in casos:
        evaluacion = evaluar_urgencia(
            float(caso["llenado"]),
            float(caso["tiempo"]),
            float(caso["afluencia"]),
        )
        resultados.append(
            {
                "identificador": caso["identificador"],
                "llenado": float(caso["llenado"]),
                "tiempo": float(caso["tiempo"]),
                "afluencia": float(caso["afluencia"]),
                "valor_urgencia": float(evaluacion.valor_urgencia),
                "etiqueta_urgencia": evaluacion.etiqueta_urgencia,
                "reglas_activadas": [regla.regla.codigo for regla in evaluacion.reglas_activadas],
                "grados_pertenencia": {
                    variable: {
                        etiqueta: float(valor)
                        for etiqueta, valor in grados.items()
                    }
                    for variable, grados in evaluacion.grados_pertenencia.items()
                },
            }
        )
    return resultados


def generar_tabla_casos(casos: Iterable[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Alias util para generar la tabla de resultados del motor difuso."""
    return ejecutar_casos_prueba(casos)


evaluar_casos_prueba = ejecutar_casos_prueba
