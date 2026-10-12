"""Transformaciones de resultados a tablas listas para mostrar o exportar."""

from __future__ import annotations

import pandas as pd


def crear_tabla_casos(resultados: list[dict]) -> pd.DataFrame:
    """Aplana los resultados difusos para su lectura en una tabla."""
    return pd.DataFrame(
        [
            {
                "Caso": resultado["identificador"],
                "Llenado (%)": resultado["llenado"],
                "Tiempo (h)": resultado["tiempo"],
                "Afluencia (%)": resultado["afluencia"],
                "Urgencia": round(resultado["valor_urgencia"], 2),
                "Etiqueta": resultado["etiqueta_urgencia"].capitalize(),
                "Reglas activadas": ", ".join(resultado["reglas_activadas"]),
            }
            for resultado in resultados
        ]
    )


def crear_tabla_experimentos(ejecuciones: list[dict], beneficio_optimo: float) -> pd.DataFrame:
    """Resume cada configuracion con media, desviacion y tasas de exito."""
    filas = []
    nombres = list(dict.fromkeys(ejecucion["configuracion"] for ejecucion in ejecuciones))
    for nombre in nombres:
        grupo = [ejecucion for ejecucion in ejecuciones if ejecucion["configuracion"] == nombre]
        beneficios = [ejecucion["beneficio"] for ejecucion in grupo]
        factibles = [ejecucion["factible"] for ejecucion in grupo]
        exitos = [factible and beneficio == beneficio_optimo for factible, beneficio in zip(factibles, beneficios)]
        filas.append(
            {
                "Configuracion": nombre,
                "Ejecuciones": len(grupo),
                "Mejor resultado": max(beneficios),
                "Beneficio medio": sum(beneficios) / len(beneficios),
                "Desviacion estandar": pd.Series(beneficios, dtype=float).std(ddof=0),
                "Factibilidad (%)": 100 * sum(factibles) / len(factibles),
                "Exito vs. optimo (%)": 100 * sum(exitos) / len(exitos),
            }
        )
    return pd.DataFrame(filas)
