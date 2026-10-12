"""Funciones de pertenencia y universos del sistema difuso."""

from __future__ import annotations

import numpy as np

from codigo.configuracion import DEFINICIONES_PERTENENCIA, LIMITES_VARIABLES


def triangular(
    universo: np.ndarray, inicio: float, pico: float, fin: float
) -> np.ndarray:
    """Devuelve una funcion de pertenencia triangular acotada entre cero y uno."""
    if not inicio <= pico <= fin or inicio == fin:
        raise ValueError("Los parametros de la funcion triangular no son validos.")

    pertenencia = np.zeros_like(universo, dtype=float)
    if inicio < pico:
        mascara_ascendente = (inicio < universo) & (universo < pico)
        pertenencia[mascara_ascendente] = (
            universo[mascara_ascendente] - inicio
        ) / (pico - inicio)
    if pico < fin:
        mascara_descendente = (pico < universo) & (universo < fin)
        pertenencia[mascara_descendente] = (
            fin - universo[mascara_descendente]
        ) / (fin - pico)

    pertenencia[np.isclose(universo, pico)] = 1.0
    return np.clip(pertenencia, 0.0, 1.0)


def trapezoidal(
    universo: np.ndarray, inicio: float, inicio_meseta: float, fin_meseta: float, fin: float
) -> np.ndarray:
    """Devuelve una funcion de pertenencia trapezoidal acotada entre cero y uno."""
    if not inicio <= inicio_meseta <= fin_meseta <= fin or inicio == fin:
        raise ValueError("Los parametros de la funcion trapezoidal no son validos.")

    pertenencia = np.zeros_like(universo, dtype=float)
    if inicio < inicio_meseta:
        mascara_ascendente = (inicio < universo) & (universo < inicio_meseta)
        pertenencia[mascara_ascendente] = (
            universo[mascara_ascendente] - inicio
        ) / (inicio_meseta - inicio)

    mascara_meseta = (inicio_meseta <= universo) & (universo <= fin_meseta)
    pertenencia[mascara_meseta] = 1.0

    if fin_meseta < fin:
        mascara_descendente = (fin_meseta < universo) & (universo < fin)
        pertenencia[mascara_descendente] = (
            fin - universo[mascara_descendente]
        ) / (fin - fin_meseta)

    return np.clip(pertenencia, 0.0, 1.0)


def construir_universos(puntos: int = 1001) -> dict[str, np.ndarray]:
    """Construye universos numericos con resolucion suficiente para el centroide."""
    if puntos < 2:
        raise ValueError("Se requieren al menos dos puntos por universo.")
    return {
        nombre: np.linspace(limite_inferior, limite_superior, puntos)
        for nombre, (limite_inferior, limite_superior) in LIMITES_VARIABLES.items()
    }


def construir_conjuntos(
    universos: dict[str, np.ndarray] | None = None,
) -> dict[str, dict[str, np.ndarray]]:
    """Construye todos los conjuntos difusos definidos para el caso."""
    universos = universos or construir_universos()
    conjuntos: dict[str, dict[str, np.ndarray]] = {}

    for variable, etiquetas in DEFINICIONES_PERTENENCIA.items():
        conjuntos[variable] = {}
        for etiqueta, (tipo, parametros) in etiquetas.items():
            if tipo == "triangular":
                conjuntos[variable][etiqueta] = triangular(universos[variable], *parametros)
            elif tipo == "trapezoidal":
                conjuntos[variable][etiqueta] = trapezoidal(universos[variable], *parametros)
            else:
                raise ValueError(f"Tipo de funcion no reconocido: {tipo}.")
    return conjuntos


def grado_en_valor(valor: float, universo: np.ndarray, conjunto: np.ndarray) -> float:
    """Obtiene por interpolacion el grado de pertenencia de un valor puntual."""
    if valor < universo[0] or valor > universo[-1]:
        raise ValueError("El valor esta fuera del universo de discurso.")
    return float(np.interp(valor, universo, conjunto))
