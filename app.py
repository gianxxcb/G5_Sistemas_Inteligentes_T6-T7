"""Interfaz Streamlit para el caso 05 de recoleccion inteligente."""

from __future__ import annotations

import pandas as pd
import numpy as np
import streamlit as st

from codigo.algoritmo_genetico.algoritmo import ejecutar_algoritmo_genetico
from codigo.algoritmo_genetico.busqueda_exhaustiva import buscar_optimo_exacto
from codigo.algoritmo_genetico.evaluacion import ACCIONES, PRESUPUESTO_MAXIMO, evaluar_cromosoma
from codigo.configuracion import DEFINICIONES_PERTENENCIA, cargar_datos
from codigo.logica_difusa.casos_prueba import CASOS_ADICIONALES, CASOS_BASE
from codigo.logica_difusa.inferencia_mamdani import evaluar_urgencia
from codigo.logica_difusa.reglas import crear_reglas_urgencia
from codigo.logica_difusa.validacion_reglas import validar_reglas_urgencia
from codigo.visualizacion.graficas_difusas import crear_figura_pertenencia, crear_figura_salida
from codigo.visualizacion.graficas_geneticas import crear_figura_convergencia
from codigo.visualizacion.tablas_resultados import crear_tabla_experimentos

DATOS = cargar_datos()
SEMILLAS = DATOS["semillas"]
OPTIMO = buscar_optimo_exacto()

st.set_page_config(page_title="Caso 05 · Clasificación de residuos", page_icon="◉", layout="wide")
st.markdown(
    """
    <style>
    :root { color-scheme: light; --verde: #176653; --tinta: #202923; --suave: #f4f7f5; --linea: #e5ebe7; }
    .stApp { background: #ffffff; color: var(--tinta); }
    [data-testid="stSidebar"] { background: var(--suave); border-right: 1px solid var(--linea); }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] { color: var(--tinta) !important; }
    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1260px; }
    h1, h2, h3 { color: var(--tinta); letter-spacing: 0; }
    h1 { font-size: 2rem; font-weight: 650; }
    h2 { font-size: 1.35rem; font-weight: 620; }
    [data-testid="stMetric"] { border: 1px solid var(--linea); border-radius: 6px; padding: 14px 16px; background: #fff; }
    [data-testid="stMetricLabel"] p { color: #65736a; font-size: .82rem; }
    [data-testid="stMetricValue"] { color: var(--verde); font-size: 1.6rem; }
    .eyebrow { color: var(--verde); font-size: .74rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
    .subtle { color: #65736a; font-size: .95rem; }
    div.stButton > button[kind="primary"] { background: var(--verde); border-color: var(--verde); }
    div.stButton > button { border-radius: 5px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def moneda(valor: float) -> str:
    """Formatea importes del caso en soles."""
    return f"S/ {valor:,.0f}"


def crear_tabla_puntos_corte() -> pd.DataFrame:
    """Expone los parametros configurados para cada funcion de pertenencia."""
    unidades = {
        "llenado": "%",
        "tiempo": "dias",
        "afluencia": "puntos",
        "urgencia": "puntos",
    }
    filas = []
    for variable, etiquetas in DEFINICIONES_PERTENENCIA.items():
        for etiqueta, (tipo, parametros) in etiquetas.items():
            forma = "triangular" if tipo == "triangular" else "trapezoidal"
            filas.append(
                {
                    "Variable": variable.capitalize(),
                    "Conjunto": etiqueta.capitalize(),
                    "Forma": forma.capitalize(),
                    f"Puntos ({unidades[variable]})": ", ".join(
                        f"{punto:g}" for punto in parametros
                    ),
                    "Criterio": "Transiciones solapadas suavizan los limites entre conjuntos; los extremos conservan pertenencia completa.",
                }
            )
    return pd.DataFrame(filas)


@st.cache_data(show_spinner=False)
def ejecutar_experimentos() -> list[dict]:
    """Corre las tres configuraciones con todas las semillas establecidas."""
    ejecuciones = []
    for configuracion in DATOS["configuraciones_ag"]:
        parametros = {
            "tamano_poblacion": configuracion["poblacion"],
            "num_generaciones": configuracion["generaciones"],
            "tasa_mutacion": configuracion["probabilidad_mutacion"],
            "probabilidad_cruce": configuracion["probabilidad_cruce"],
            "tamano_torneo": min(3, configuracion["poblacion"]),
        }
        for semilla in SEMILLAS:
            resultado = ejecutar_algoritmo_genetico(parametros, semilla)
            ejecuciones.append(
                {
                    "configuracion": configuracion["nombre"],
                    "semilla": semilla,
                    "cromosoma": resultado["cromosoma_ganador"],
                    "beneficio": resultado["beneficio"],
                    "costo": resultado["inversion"],
                    "factible": resultado["inversion"] <= PRESUPUESTO_MAXIMO,
                    "historial": resultado["historial"],
                    "acciones": resultado["acciones_elegidas"],
                }
            )
    return ejecuciones


def mostrar_resumen() -> None:
    st.markdown('<p class="eyebrow">Caso 05 · Sistemas inteligentes</p>', unsafe_allow_html=True)
    st.title("Clasificación de residuos y optimización de acciones ambientales")
    st.markdown('<p class="subtle">El clasificador estima urgencia de recolección; el optimizador selecciona iniciativas ambientales bajo presupuesto.</p>', unsafe_allow_html=True)
    validacion = validar_reglas_urgencia()
    metricas = st.columns(4)
    metricas[0].metric("Presupuesto maximo", moneda(PRESUPUESTO_MAXIMO))
    metricas[1].metric("Acciones disponibles", len(ACCIONES))
    metricas[2].metric("Reglas difusas", validacion["total_reglas"])
    metricas[3].metric("Optimo exacto", f'{OPTIMO["optimo"]["beneficio"]:.0f} pts')

    st.divider()
    st.subheader("Alcance del caso")
    st.info("La salida de la lógica difusa clasifica la urgencia de recolección (baja, media o alta); no identifica el material del residuo. Sus entradas son llenado, días desde la última recolección y afluencia.")
    izquierda, derecha = st.columns([1.15, 0.85], gap="large")
    with izquierda:
        st.subheader("Mejor combinacion encontrada")
        st.markdown(f"### {OPTIMO['optimo']['beneficio']:.0f} puntos de beneficio")
        st.markdown(f"Inversion de **{moneda(OPTIMO['optimo']['costo'])}** sobre {moneda(PRESUPUESTO_MAXIMO)}.")
        st.progress(min(OPTIMO["optimo"]["costo"] / PRESUPUESTO_MAXIMO, 1.0))
        elegidas = OPTIMO["optimo"]["acciones_detalle"]
        st.dataframe(
            pd.DataFrame([{"Codigo": accion["codigo"], "Accion": accion["nombre"]} for accion in elegidas]),
            hide_index=True,
            width="stretch",
        )
    with derecha:
        st.subheader("Estado del sistema")
        if validacion["cobertura_completa"]:
            st.success("Base de reglas completa y sin contradicciones.")
        else:
            st.warning("La base de reglas requiere revision.")
        st.markdown("**Entradas difusas**")
        st.caption("Llenado (0-100 %) · tiempo (0-10 dias) · afluencia (0-100 puntos)")
        st.markdown("**Optimizacion ambiental**")
        st.caption("Ocho acciones indivisibles · beneficios en puntos · presupuesto maximo S/ 19 000")


def mostrar_logica_difusa() -> None:
    st.markdown('<p class="eyebrow">Motor Mamdani</p>', unsafe_allow_html=True)
    st.title("Clasificación de urgencia de recolección")
    st.caption("Ajusta los datos de un sector y consulta la inferencia Mamdani completa.")
    entrada = st.columns(3)
    llenado = entrada[0].slider("Nivel de llenado", 0, 100, 72, format="%d%%")
    tiempo = entrada[1].slider("Días desde última recolección", 0.0, 10.0, 6.0, 0.5, format="%.1f dias")
    afluencia = entrada[2].slider("Afluencia de personas", 0, 100, 58, format="%d puntos")
    resultado = evaluar_urgencia(llenado, tiempo, afluencia)

    resumen = st.columns([0.8, 1.5, 1.5])
    resumen[0].metric("Urgencia", f"{resultado.valor_urgencia:.1f}/100", resultado.etiqueta_urgencia.capitalize())
    resumen[1].dataframe(
        pd.DataFrame([{"Variable": variable.capitalize(), "Conjunto": etiqueta.capitalize(), "Grado": round(grado, 3)} for variable, grados in resultado.grados_pertenencia.items() for etiqueta, grado in grados.items()]),
        hide_index=True,
        width="stretch",
        height=175,
    )
    resumen[2].pyplot(crear_figura_salida(resultado), width="stretch")

    with st.expander("Etapas de inferencia Mamdani"):
        st.markdown(
            "1. **Fuzzificación:** interpola el grado de pertenencia de cada entrada en sus conjuntos lingüísticos.  \n"
            "2. **Conjunción:** toma el mínimo de los tres grados para cada regla.  \n"
            "3. **Implicación:** recorta el conjunto de salida al nivel de activación de la regla (mínimo).  \n"
            "4. **Agregación:** combina las salidas de las reglas activadas mediante el máximo.  \n"
            "5. **Desfusificación:** calcula el centroide discreto de la salida agregada."
        )
        st.latex(r"u^* = \frac{\sum_i u_i\,\mu_{agregada}(u_i)}{\sum_i \mu_{agregada}(u_i)}")

    with st.expander("Reglas activadas", expanded=True):
        reglas = [
            {
                "Regla": activacion.regla.codigo,
                "Antecedente": f"{activacion.regla.llenado} + {activacion.regla.tiempo} + {activacion.regla.afluencia}",
                "Consecuencia": activacion.regla.urgencia.capitalize(),
                "Activacion": round(activacion.intensidad, 3),
            }
            for activacion in resultado.reglas_activadas
        ]
        st.dataframe(pd.DataFrame(reglas), hide_index=True, width="stretch")

    with st.expander("Funciones de pertenencia y puntos de corte", expanded=True):
        st.caption("Los puntos corresponden a las funciones triangulares y trapezoidales configuradas. El solapamiento permite transiciones graduales entre etiquetas; los extremos se mantienen cubiertos.")
        st.dataframe(crear_tabla_puntos_corte(), hide_index=True, width="stretch")
        columnas = st.columns(3)
        for columna, variable in zip(columnas, ("llenado", "tiempo", "afluencia")):
            columna.pyplot(crear_figura_pertenencia(variable), width="stretch")

    with st.expander("Base de reglas y validación"):
        reglas = crear_reglas_urgencia()
        st.caption(f"La base contiene {len(reglas)} reglas SI-ENTONCES; el mínimo solicitado por el caso es 10.")
        tabla_reglas = pd.DataFrame(
            [
                {
                    "Regla": regla.codigo,
                    "Si llenado": regla.llenado,
                    "Y tiempo": regla.tiempo,
                    "Y afluencia": regla.afluencia,
                    "Entonces urgencia": regla.urgencia,
                }
                for regla in reglas
            ]
        )
        st.dataframe(tabla_reglas, hide_index=True, width="stretch")
        validacion = validar_reglas_urgencia()
        if validacion["cobertura_completa"]:
            st.success("Cobertura de las 27 combinaciones completa; no hay antecedentes duplicados con consecuencias contradictorias.")
        else:
            st.warning(f"Combinaciones faltantes: {len(validacion['faltantes'])} · contradicciones: {len(validacion['contradicciones'])}.")


def mostrar_registros_prueba() -> None:
    st.markdown('<p class="eyebrow">Evaluación reproducible</p>', unsafe_allow_html=True)
    st.title("Registros y pruebas adicionales")
    st.caption("Los cinco registros del enunciado y dos casos adicionales calculados por el motor.")
    casos = CASOS_BASE + CASOS_ADICIONALES
    resultados = {}
    filas = []
    for caso in casos:
        resultado = evaluar_urgencia(caso["llenado"], caso["tiempo"], caso["afluencia"])
        resultados[caso["identificador"]] = resultado
        filas.append(
            {
                "ID": caso["identificador"],
                "Llenado (%)": caso["llenado"],
                "Tiempo (dias)": caso["tiempo"],
                "Afluencia (puntos)": caso["afluencia"],
                "Urgencia (0-100)": round(resultado.valor_urgencia, 2),
                "Clase": resultado.etiqueta_urgencia.capitalize(),
                "Reglas activadas": ", ".join(activacion.regla.codigo for activacion in resultado.reglas_activadas),
            }
        )
    tabla = pd.DataFrame(filas)
    st.dataframe(tabla, hide_index=True, width="stretch")
    st.download_button("Descargar resultados CSV", tabla.to_csv(index=False).encode("utf-8-sig"), "caso_05_registros.csv", "text/csv")

    identificador = st.selectbox("Inspeccionar trazabilidad", list(resultados))
    resultado = resultados[identificador]
    entradas_dominantes = {
        variable: max(etiquetas, key=etiquetas.get)
        for variable, etiquetas in resultado.grados_pertenencia.items()
    }
    st.caption(
        f"{identificador}: los conjuntos dominantes son llenado {entradas_dominantes['llenado']}, "
        f"tiempo {entradas_dominantes['tiempo']} y afluencia {entradas_dominantes['afluencia']}; "
        f"se activan {len(resultado.reglas_activadas)} reglas. El centroide produce "
        f"{resultado.valor_urgencia:.2f}/100 ({resultado.etiqueta_urgencia})."
    )
    izquierda, derecha = st.columns([1, 1.6])
    with izquierda:
        st.metric("Urgencia calculada", f"{resultado.valor_urgencia:.2f}/100", resultado.etiqueta_urgencia.capitalize())
        grados = pd.DataFrame(
            [
                {"Variable": variable.capitalize(), "Etiqueta": etiqueta.capitalize(), "Pertenencia": round(valor, 4)}
                for variable, etiquetas in resultado.grados_pertenencia.items()
                for etiqueta, valor in etiquetas.items()
            ]
        )
        st.dataframe(grados, hide_index=True, width="stretch")
    with derecha:
        st.pyplot(crear_figura_salida(resultado), width="stretch")

    activaciones = pd.DataFrame(
        [
            {
                "Regla": activacion.regla.codigo,
                "Antecedentes": f"{activacion.regla.llenado} + {activacion.regla.tiempo} + {activacion.regla.afluencia}",
                "Consecuencia": activacion.regla.urgencia.capitalize(),
                "Intensidad": round(activacion.intensidad, 4),
            }
            for activacion in resultado.reglas_activadas
        ]
    )
    st.subheader(f"Reglas activadas · {identificador}")
    st.dataframe(activaciones, hide_index=True, width="stretch")
    universo_salida = np.linspace(0, 100, len(resultado.salida_agregada))
    salida_agregada = pd.DataFrame(
        {"Urgencia": universo_salida, "Pertenencia agregada": resultado.salida_agregada}
    )
    with st.expander("Valores de la salida agregada"):
        st.dataframe(salida_agregada, hide_index=True, width="stretch", height=260)
        st.download_button(
            "Descargar salida agregada CSV",
            salida_agregada.to_csv(index=False).encode("utf-8-sig"),
            f"salida_agregada_{identificador}.csv",
            "text/csv",
        )


def mostrar_optimizacion() -> None:
    st.markdown('<p class="eyebrow">Evaluacion de soluciones</p>', unsafe_allow_html=True)
    st.title("Optimización de acciones ambientales")
    st.caption("Explora una combinacion y contrasta sus resultados con el optimo exacto de las 256 posibilidades.")
    ejemplo = evaluar_cromosoma("01110110")
    st.info(
        f"Ejemplo del caso · cromosoma 01110110 · inversion {moneda(ejemplo['costo'])} · "
        f"beneficio {ejemplo['beneficio']:.0f} puntos · "
        f"{'factible' if ejemplo['factible'] else 'no factible'}."
    )
    st.caption("Los beneficios son indices comparativos en puntos, no montos monetarios. Cada gen representa una accion indivisible.")
    cabecera = st.columns([3, 1, 1])
    cabecera[0].markdown("**Acción**")
    cabecera[1].markdown("**Costo**")
    cabecera[2].markdown("**Beneficio**")
    genes = []
    for accion in ACCIONES:
        fila = st.columns([3, 1, 1])
        seleccionada = fila[0].checkbox(
            f"{accion['codigo']} · {accion['nombre']}",
            key=f"seleccion_{accion['codigo']}",
        )
        fila[1].write(moneda(float(accion["costo"])))
        fila[2].write(f"{accion['beneficio']} puntos")
        genes.append(int(seleccionada))
    cromosoma = tuple(genes)
    evaluacion = evaluar_cromosoma(cromosoma)
    metricas = st.columns(4)
    metricas[0].metric("Inversion", moneda(evaluacion["costo"]))
    metricas[1].metric("Beneficio", f'{evaluacion["beneficio"]:.0f} puntos')
    metricas[2].metric("Saldo", moneda(PRESUPUESTO_MAXIMO - evaluacion["costo"]))
    metricas[3].metric("Estado", "Factible" if evaluacion["factible"] else "Excede presupuesto")
    st.progress(min(evaluacion["costo"] / PRESUPUESTO_MAXIMO, 1.0))
    if not evaluacion["factible"]:
        st.error(f"La combinacion excede el presupuesto en {moneda(evaluacion['exceso'])}.")

    st.divider()
    izquierda, derecha = st.columns(2)
    with izquierda:
        st.subheader("Tu combinacion")
        st.code("".join(map(str, cromosoma)), language=None)
        elegidas = evaluacion["acciones_detalle"]
        if elegidas:
            st.dataframe(pd.DataFrame([{"Codigo": accion["codigo"], "Accion": accion["nombre"], "Costo": moneda(accion["costo"]), "Beneficio": accion["beneficio"]} for accion in elegidas]), hide_index=True, width="stretch")
        else:
            st.info("Selecciona una o mas acciones para evaluar la combinacion.")
    with derecha:
        st.subheader("Optimo exacto")
        st.metric("Beneficio maximo", f'{OPTIMO["optimo"]["beneficio"]:.0f} puntos', f'{OPTIMO["optimo"]["costo"]:,.0f} S/ de inversion')
        st.caption(f"Cromosoma ganador: {''.join(map(str, OPTIMO['mejor_cromosoma']))}")
        diferencia = OPTIMO["optimo"]["beneficio"] - evaluacion["beneficio"]
        st.caption(f"Diferencia de beneficio: {diferencia:.0f} puntos")


def mostrar_experimentos() -> None:
    st.markdown('<p class="eyebrow">Experimentos reproducibles</p>', unsafe_allow_html=True)
    st.title("Comparacion del algoritmo genetico")
    st.caption(f"Configuraciones A, B y C · semillas {', '.join(map(str, SEMILLAS))} · referencia exacta de {OPTIMO['optimo']['beneficio']:.0f} puntos.")
    configuraciones = pd.DataFrame(
        [{"Configuracion": config["nombre"], "Poblacion": config["poblacion"], "Cruce": config["probabilidad_cruce"], "Mutacion": config["probabilidad_mutacion"], "Generaciones": config["generaciones"]} for config in DATOS["configuraciones_ag"]]
    )
    st.dataframe(configuraciones, hide_index=True, width="stretch")
    st.caption("Fitness factible = beneficio. Fitness inviable = beneficio - 1 000 000 × exceso de presupuesto (S/). La mutación se aplica por gen y se conserva un individuo élite por generación.")
    with st.expander("Operadores genéticos"):
        st.markdown(
            "- **Población inicial:** cromosomas binarios aleatorios de ocho genes.  \n"
            "- **Selección:** torneo de tres individuos.  \n"
            "- **Cruce:** cruce de un punto según la probabilidad de cada configuración.  \n"
            "- **Mutación:** inversión de cada bit con la probabilidad indicada.  \n"
            "- **Elitismo:** conserva el individuo de mayor fitness de cada generación."
        )
    if st.button("Ejecutar 15 experimentos", type="primary"):
        with st.spinner("Ejecutando las configuraciones y semillas..."):
            st.session_state["ejecuciones_ag"] = ejecutar_experimentos()

    ejecuciones = st.session_state.get("ejecuciones_ag")
    if not ejecuciones:
        st.info("Ejecuta el experimento para generar las metricas y curvas de convergencia.")
        return

    resumen = crear_tabla_experimentos(ejecuciones, OPTIMO["optimo"]["beneficio"])
    st.subheader("Resumen comparativo")
    st.dataframe(
        resumen.style.format({"Mejor resultado": "{:.0f}", "Beneficio medio": "{:.2f}", "Desviacion estandar": "{:.2f}", "Factibilidad (%)": "{:.0f}%", "Exito vs. optimo (%)": "{:.0f}%"}),
        hide_index=True,
        width="stretch",
    )
    st.download_button("Descargar resumen CSV", resumen.to_csv(index=False).encode("utf-8-sig"), "resumen_experimentos.csv", "text/csv")

    st.subheader("Resultados por semilla")
    detalle = pd.DataFrame(
        [{"Configuracion": corrida["configuracion"], "Semilla": corrida["semilla"], "Cromosoma": "".join(map(str, corrida["cromosoma"])) if corrida["cromosoma"] else "Sin solucion", "Beneficio": corrida["beneficio"], "Inversion": corrida["costo"], "Saldo": PRESUPUESTO_MAXIMO - corrida["costo"], "Factible": corrida["factible"], "Acciones": ", ".join(corrida["acciones"])} for corrida in ejecuciones]
    )
    st.dataframe(detalle, hide_index=True, width="stretch")
    indice = st.selectbox(
        "Curva de convergencia",
        range(len(ejecuciones)),
        format_func=lambda posicion: f"Configuracion {ejecuciones[posicion]['configuracion']} · semilla {ejecuciones[posicion]['semilla']}",
    )
    corrida = ejecuciones[indice]
    izquierda, derecha = st.columns([1.5, 1])
    izquierda.pyplot(crear_figura_convergencia(corrida["historial"]), width="stretch")
    derecha.metric("Mejor beneficio", f"{corrida['beneficio']:.0f} puntos", "Optimo alcanzado" if corrida["beneficio"] == OPTIMO["optimo"]["beneficio"] else "Por debajo del optimo")
    derecha.metric("Inversion", moneda(corrida["costo"]))
    derecha.caption(f"Mejor cromosoma: {''.join(map(str, corrida['cromosoma'])) if corrida['cromosoma'] else 'No disponible'}")


def mostrar_integracion() -> None:
    st.markdown('<p class="eyebrow">Análisis del caso</p>', unsafe_allow_html=True)
    st.title("Integración y limitaciones")
    st.caption("Relación entre la inferencia difusa para priorizar sectores y la optimización de acciones ambientales.")
    with st.expander("¿Cuándo elevar la urgencia con poco llenado?", expanded=True):
        st.write("Cuando el tiempo desde la última recolección sea largo o la afluencia alta. La base incluye, por ejemplo, reglas de urgencia alta para bajo llenado combinado con tiempo largo y afluencia media o alta.")
    with st.expander("¿Cómo comprobar que las reglas no se contradicen?"):
        st.write("Se valida cobertura de las 27 combinaciones lingüísticas y se busca que ningún antecedente repetido tenga consecuencias diferentes. Esta comprobación estructural se complementa revisando casos límite y la coherencia de las reglas con el contexto municipal.")
    with st.expander("¿Qué limitación tiene un único beneficio numérico?"):
        st.write("Resume impactos distintos en una sola escala: puede ocultar diferencias entre reducción de residuos, emisiones, salud pública y equidad territorial. Los valores del caso son índices estimados, no mediciones monetarias ni impactos observados.")
    with st.expander("¿Cómo integrar la urgencia en el fitness?"):
        st.write("Como extensión, cada acción podría asociarse a sectores y ponderarse por su urgencia difusa, maximizando el impacto priorizado sujeto al presupuesto. El caso no proporciona una matriz sector-acción ni costos por sector, por lo que esa variante no se calcula en esta app.")
    with st.expander("¿Qué problema resuelve cada técnica?"):
        st.write("La lógica difusa convierte entradas imprecisas del sector en una urgencia interpretable mediante reglas. El algoritmo genético explora combinaciones discretas de iniciativas para maximizar beneficios sin exceder el presupuesto; la enumeración exacta permite verificar el óptimo para ocho acciones.")
    with st.expander("Convergencia prematura y mejora propuesta"):
        st.write("La selección por torneo y el elitismo pueden reducir diversidad y fijar pronto una población en una solución subóptima. Una mejora verificable sería comparar varios tamaños de torneo o una mutación adaptativa, manteniendo semillas, presupuesto y búsqueda exhaustiva como referencia.")


with st.sidebar:
    st.markdown('<p class="eyebrow">Caso 05</p>', unsafe_allow_html=True)
    st.markdown("## Sistema inteligente")
    seccion = st.radio("Navegacion", ["Resumen", "Clasificacion de urgencia", "Registros de prueba", "Optimizacion", "Experimentos", "Integracion y limites"], label_visibility="collapsed")
    st.divider()
    st.caption("Motor Mamdani · Algoritmo genetico · Busqueda exacta")

if seccion == "Resumen":
    mostrar_resumen()
elif seccion == "Clasificacion de urgencia":
    mostrar_logica_difusa()
elif seccion == "Registros de prueba":
    mostrar_registros_prueba()
elif seccion == "Optimizacion":
    mostrar_optimizacion()
elif seccion == "Experimentos":
    mostrar_experimentos()
else:
    mostrar_integracion()
