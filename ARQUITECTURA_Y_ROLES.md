# Arquitectura y division del proyecto

## Flujo lineal

El integrante 1 entrega el motor difuso y los datos comunes. El integrante 2 usa ese motor para procesar los casos y prepara la evaluacion del problema de optimizacion. El integrante 3 usa esa evaluacion para ejecutar el algoritmo genetico. El integrante 4 usa los resultados de los tres anteriores para generar graficas, tablas y el cuaderno final.

## Integrante 1 - Base comun y motor de logica difusa

Archivos a cargo:

- `datos/caso_05.json`
- `codigo/configuracion.py`
- `codigo/logica_difusa/funciones_pertenencia.py`
- `codigo/logica_difusa/reglas.py`
- `codigo/logica_difusa/inferencia_mamdani.py`
- `pruebas/prueba_logica_difusa.py`

Debe implementar funciones triangulares y trapezoidales, universos de discurso, 27 reglas coherentes, fuzzificacion, conjuncion minimo, implicacion minimo, agregacion maximo y desfusificacion por centroide. Su contrato de salida es `evaluar_urgencia(llenado, tiempo, afluencia)`, que devuelve grados de pertenencia, reglas activadas, salida agregada, valor numerico y etiqueta de urgencia.

## Integrante 2 - Validacion difusa y evaluacion de soluciones

Archivos a cargo:

- `codigo/logica_difusa/casos_prueba.py`
- `codigo/logica_difusa/validacion_reglas.py`
- `codigo/algoritmo_genetico/evaluacion.py`
- `codigo/algoritmo_genetico/busqueda_exhaustiva.py`
- `pruebas/prueba_evaluacion.py`

Debe ejecutar R01-R05 y dos casos nuevos utilizando la funcion del integrante 1. Debe preparar tablas con grados y reglas activadas, comprobar cobertura o posibles contradicciones de reglas y crear la representacion binaria de ocho genes. Tambien debe calcular costo, beneficio, factibilidad, fitness penalizado y el optimo exacto de las 256 combinaciones. Su contrato de salida es una evaluacion estructurada de cada cromosoma y el optimo exacto verificable.

## Integrante 3 - Algoritmo genetico

Archivos a cargo:

- `codigo/algoritmo_genetico/operadores.py`
- `codigo/algoritmo_genetico/algoritmo.py`
- `pruebas/prueba_algoritmo_genetico.py`

Debe usar el evaluador del integrante 2 para generar poblacion aleatoria, seleccionar por torneo, cruzar en un punto, mutar cada gen por inversion de bit y conservar al menos un elite. Debe registrar por generacion el mejor fitness factible, el fitness promedio, el porcentaje de factibilidad y el mejor cromosoma. Su contrato de salida es el historial completo de una ejecucion reproducible con semilla.

## Integrante 4 - Visualizacion, experimentos y cuaderno final

Archivos a cargo:

- `codigo/visualizacion/graficas_difusas.py`
- `codigo/visualizacion/graficas_geneticas.py`
- `codigo/visualizacion/tablas_resultados.py`
- `codigo/experimentos.py`
- `cuadernos/trabajo_caso_05.ipynb`

Debe ser responsable solo de la capa visual y los archivos directamente asociados: graficas de pertenencia, salida agregada, curvas de convergencia y tablas finales. Debe ejecutar las configuraciones A, B y C con cinco semillas, reunir media, desviacion estandar, tasa de factibilidad y tasa de exito, y presentar el cromosoma ganador frente al optimo exacto. El cuaderno importa los modulos anteriores, no duplica algoritmos, y muestra los resultados visibles para Google Colab.

## Reglas de integracion

- Todos los nombres de variables, funciones, mensajes y comentarios se escriben en espanol sin tildes ni espacios en identificadores.
- Se permite `numpy`, `pandas` y `matplotlib`; no se permite usar paquetes que automaticen la logica difusa o el algoritmo genetico.
- Las semillas son `11, 22, 33, 44 y 55` y se deben reportar en los experimentos.
- Ningun cromosoma con costo mayor a S/ 19 000 puede informarse como solucion factible.
- Los resultados se producen por ejecucion del codigo; no se escriben manualmente.
