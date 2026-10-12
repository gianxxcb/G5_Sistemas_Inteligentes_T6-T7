"""Motor de inferencia Mamdani para la urgencia de recoleccion."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from codigo.configuracion import LIMITES_VARIABLES
from codigo.logica_difusa.funciones_pertenencia import (
    construir_conjuntos,
    construir_universos,
    grado_en_valor,
)
from codigo.logica_difusa.reglas import ReglaDifusa, crear_reglas_urgencia


@dataclass(frozen=True)
class ReglaActivada:
    """Regla y nivel de activacion obtenido durante la inferencia."""

    regla: ReglaDifusa
    intensidad: float


@dataclass
class ResultadoUrgencia:
    """Trazabilidad completa de una evaluacion Mamdani."""

    entradas: dict[str, float]
    grados_pertenencia: dict[str, dict[str, float]]
    reglas_activadas: tuple[ReglaActivada, ...]
    salida_agregada: np.ndarray
    valor_urgencia: float
    etiqueta_urgencia: str


def validar_entradas(entradas: dict[str, float]) -> None:
    """Verifica que todas las entradas existan y pertenezcan a su dominio."""
    for variable in ("llenado", "tiempo", "afluencia"):
        if variable not in entradas:
            raise ValueError(f"Falta la entrada obligatoria: {variable}.")
        limite_inferior, limite_superior = LIMITES_VARIABLES[variable]
        valor = entradas[variable]
        if not limite_inferior <= valor <= limite_superior:
            raise ValueError(
                f"{variable} debe estar entre {limite_inferior} y {limite_superior}."
            )


def fuzzificar(
    entradas: dict[str, float],
    universos: dict[str, np.ndarray],
    conjuntos: dict[str, dict[str, np.ndarray]],
) -> dict[str, dict[str, float]]:
    """Calcula los grados de pertenencia de las tres entradas del caso."""
    return {
        variable: {
            etiqueta: grado_en_valor(entradas[variable], universos[variable], conjunto)
            for etiqueta, conjunto in conjuntos[variable].items()
        }
        for variable in ("llenado", "tiempo", "afluencia")
    }


def activar_reglas(
    grados_pertenencia: dict[str, dict[str, float]], reglas: tuple[ReglaDifusa, ...]
) -> tuple[ReglaActivada, ...]:
    """Aplica la conjuncion minimo a cada regla de la base de conocimiento."""
    activaciones = []
    for regla in reglas:
        intensidad = min(
            grados_pertenencia["llenado"][regla.llenado],
            grados_pertenencia["tiempo"][regla.tiempo],
            grados_pertenencia["afluencia"][regla.afluencia],
        )
        if intensidad > 0.0:
            activaciones.append(ReglaActivada(regla, intensidad))
    return tuple(activaciones)


def agregar_salidas(
    activaciones: tuple[ReglaActivada, ...], conjuntos_urgencia: dict[str, np.ndarray]
) -> np.ndarray:
    """Aplica implicacion minimo y agregacion maximo a las reglas activadas."""
    salida_agregada = np.zeros_like(next(iter(conjuntos_urgencia.values())), dtype=float)
    for activacion in activaciones:
        salida_recortada = np.minimum(
            activacion.intensidad, conjuntos_urgencia[activacion.regla.urgencia]
        )
        salida_agregada = np.maximum(salida_agregada, salida_recortada)
    return salida_agregada


def desfusificar_centroide(universo: np.ndarray, salida_agregada: np.ndarray) -> float:
    """Convierte la salida difusa agregada en un valor numerico por centroide."""
    denominador = float(np.sum(salida_agregada))
    if denominador == 0.0:
        raise ValueError("No hay reglas activadas para obtener el centroide.")
    return float(np.sum(universo * salida_agregada) / denominador)


def etiquetar_urgencia(
    valor_urgencia: float, universo: np.ndarray, conjuntos_urgencia: dict[str, np.ndarray]
) -> str:
    """Asigna la etiqueta con mayor pertenencia al valor final de urgencia."""
    grados = {
        etiqueta: grado_en_valor(valor_urgencia, universo, conjunto)
        for etiqueta, conjunto in conjuntos_urgencia.items()
    }
    return max(grados, key=grados.get)


def evaluar_urgencia(
    llenado: float, tiempo: float, afluencia: float
) -> ResultadoUrgencia:
    """Ejecuta todas las etapas Mamdani y devuelve resultados trazables."""
    entradas = {"llenado": float(llenado), "tiempo": float(tiempo), "afluencia": float(afluencia)}
    validar_entradas(entradas)
    universos = construir_universos()
    conjuntos = construir_conjuntos(universos)
    grados_pertenencia = fuzzificar(entradas, universos, conjuntos)
    reglas_activadas = activar_reglas(grados_pertenencia, crear_reglas_urgencia())
    salida_agregada = agregar_salidas(reglas_activadas, conjuntos["urgencia"])
    valor_urgencia = desfusificar_centroide(universos["urgencia"], salida_agregada)
    etiqueta_urgencia = etiquetar_urgencia(
        valor_urgencia, universos["urgencia"], conjuntos["urgencia"]
    )
    return ResultadoUrgencia(
        entradas=entradas,
        grados_pertenencia=grados_pertenencia,
        reglas_activadas=reglas_activadas,
        salida_agregada=salida_agregada,
        valor_urgencia=valor_urgencia,
        etiqueta_urgencia=etiqueta_urgencia,
    )
