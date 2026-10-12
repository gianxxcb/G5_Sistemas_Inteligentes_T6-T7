"""Graficas para analizar la convergencia del algoritmo genetico."""

from __future__ import annotations

import matplotlib.pyplot as plt


def crear_figura_convergencia(historial: list[dict]) -> plt.Figure:
    """Compara fitness promedio y mejor fitness factible por generacion."""
    figura, eje = plt.subplots(figsize=(8, 3.5), layout="constrained")
    generaciones = [registro["generacion"] for registro in historial]
    mejor = [registro["mejor_fitness_factible"] for registro in historial]
    promedio = [registro["fitness_promedio"] for registro in historial]
    eje.plot(generaciones, mejor, color="#176653", linewidth=2.4, label="Mejor factible")
    eje.plot(generaciones, promedio, color="#e6a23c", linewidth=1.7, label="Promedio de poblacion")
    eje.set_title("Evolucion del algoritmo genetico", loc="left", fontsize=12, fontweight="semibold")
    eje.set_xlabel("Generacion")
    eje.set_ylabel("Fitness")
    eje.grid(axis="y", color="#e9eeeb", linewidth=0.8)
    eje.spines[["top", "right"]].set_visible(False)
    eje.legend(frameon=False)
    return figura
