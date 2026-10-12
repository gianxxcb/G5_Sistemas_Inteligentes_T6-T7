"""Graficas de pertenencia e inferencia para la interfaz del caso 05."""

from __future__ import annotations

import matplotlib.pyplot as plt

from codigo.configuracion import DEFINICIONES_PERTENENCIA
from codigo.logica_difusa.funciones_pertenencia import construir_conjuntos, construir_universos

COLORES = {"baja": "#25836d", "bajo": "#25836d", "corto": "#25836d", "media": "#e6a23c", "medio": "#e6a23c", "alta": "#d66a56", "alto": "#d66a56", "largo": "#d66a56"}
UNIDADES = {"llenado": "%", "tiempo": "dias", "afluencia": "puntos", "urgencia": "puntos"}


def crear_figura_pertenencia(variable: str) -> plt.Figure:
    """Dibuja los conjuntos difusos de una variable del caso."""
    universos = construir_universos()
    conjuntos = construir_conjuntos(universos)
    figura, eje = plt.subplots(figsize=(8, 3.5), layout="constrained")
    eje.set_facecolor("#ffffff")
    for etiqueta, pertenencia in conjuntos[variable].items():
        eje.plot(universos[variable], pertenencia, linewidth=2.2, color=COLORES[etiqueta], label=etiqueta.capitalize())
    eje.set_title(f"Funciones de pertenencia · {variable.capitalize()}", loc="left", fontsize=12, fontweight="semibold")
    eje.set_xlabel(f"Valor ({UNIDADES[variable]})")
    eje.set_ylabel("Grado de pertenencia (0-1)")
    eje.set_ylim(-0.04, 1.08)
    eje.grid(axis="y", color="#e9eeeb", linewidth=0.8)
    eje.spines[["top", "right"]].set_visible(False)
    eje.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, -0.17))
    return figura


def crear_figura_salida(resultado) -> plt.Figure:
    """Muestra conjuntos de salida, agregado Mamdani y centroide."""
    universos = construir_universos()
    conjuntos = construir_conjuntos(universos)["urgencia"]
    universo = universos["urgencia"]
    figura, eje = plt.subplots(figsize=(8, 3.5), layout="constrained")
    eje.set_facecolor("#ffffff")
    for etiqueta, pertenencia in conjuntos.items():
        eje.plot(universo, pertenencia, color=COLORES[etiqueta], linewidth=1.7, alpha=0.72, label=f"{etiqueta.capitalize()} (base)")
    eje.fill_between(universo, resultado.salida_agregada, color="#25836d", alpha=0.2, label="Salida agregada")
    eje.plot(universo, resultado.salida_agregada, color="#176653", linewidth=2.5)
    eje.axvline(resultado.valor_urgencia, color="#d66a56", linestyle="--", linewidth=1.8, label=f"Centroide {resultado.valor_urgencia:.1f}")
    eje.set_title("Agregacion Mamdani y desfusificacion", loc="left", fontsize=12, fontweight="semibold")
    eje.set_xlabel(f"Urgencia ({UNIDADES['urgencia']})")
    eje.set_ylabel("Grado de pertenencia (0-1)")
    eje.set_ylim(-0.04, 1.08)
    eje.grid(axis="y", color="#e9eeeb", linewidth=0.8)
    eje.spines[["top", "right"]].set_visible(False)
    eje.legend(frameon=False, ncols=2, loc="upper center", bbox_to_anchor=(0.5, -0.17))
    return figura
