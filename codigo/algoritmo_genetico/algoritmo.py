import random
from codigo.algoritmo_genetico.operadores import (
    generar_poblacion, seleccion_torneo, cruce_un_punto, 
    mutacion_inversion_bits, aplicar_elitismo
)
from codigo.algoritmo_genetico.evaluacion import evaluar_cromosoma, PRESUPUESTO_MAXIMO

def ejecutar_algoritmo_genetico(configuracion, semilla):
    random.seed(semilla)
    
    tamano_poblacion = configuracion.get("tamano_poblacion", 20)
    num_generaciones = configuracion.get("num_generaciones", 50)
    tasa_mutacion = configuracion.get("tasa_mutacion", 0.1)
    tamano_torneo = configuracion.get("tamano_torneo", 3)
    probabilidad_cruce = configuracion.get("probabilidad_cruce", 1.0)
    longitud_cromosoma = 8
    
    poblacion = generar_poblacion(tamano_poblacion, longitud_cromosoma, semilla)
    historial = []
    mejor_cromosoma_global = None
    mejor_resultado_global = {"fitness": -1}
    
    for generacion in range(num_generaciones):
        resultados_evaluacion = [evaluar_cromosoma(ind) for ind in poblacion]
        lista_fitness = [res["fitness"] for res in resultados_evaluacion]
        
        # Metricas de la generacion
        factibles = [res for res in resultados_evaluacion if res["factible"]]
        porcentaje_factibilidad = (len(factibles) / tamano_poblacion) * 100
        fitness_promedio = sum(lista_fitness) / tamano_poblacion
        
        if factibles:
            mejor_factible = max(factibles, key=lambda x: x["fitness"])
        else:
            mejor_factible = {"fitness": 0, "acciones": []}
            
        indice_mejor = lista_fitness.index(max(lista_fitness))
        mejor_cromosoma_gen = poblacion[indice_mejor]
        
        if resultados_evaluacion[indice_mejor]["fitness"] > mejor_resultado_global["fitness"] and resultados_evaluacion[indice_mejor]["factible"]:
            mejor_resultado_global = resultados_evaluacion[indice_mejor]
            mejor_cromosoma_global = mejor_cromosoma_gen
            
        historial.append({
            "generacion": generacion + 1,
            "mejor_fitness_factible": mejor_factible["fitness"],
            "fitness_promedio": fitness_promedio,
            "porcentaje_factibilidad": porcentaje_factibilidad,
            "mejor_cromosoma": mejor_cromosoma_gen
        })
        
        # Nueva poblacion
        nueva_poblacion = []
        
        # Conservar al menos un individuo elite
        elite = aplicar_elitismo(poblacion, lista_fitness)
        nueva_poblacion.append(elite)
        
        while len(nueva_poblacion) < tamano_poblacion:
            padre1 = seleccion_torneo(poblacion, lista_fitness, tamano_torneo)
            padre2 = seleccion_torneo(poblacion, lista_fitness, tamano_torneo)
            
            if random.random() < probabilidad_cruce:
                hijo1, hijo2 = cruce_un_punto(padre1, padre2)
            else:
                hijo1, hijo2 = padre1[:], padre2[:]
            
            hijo1 = mutacion_inversion_bits(hijo1, tasa_mutacion)
            hijo2 = mutacion_inversion_bits(hijo2, tasa_mutacion)
            
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < tamano_poblacion:
                nueva_poblacion.append(hijo2)
                
        poblacion = nueva_poblacion
        
    presupuesto_restante = PRESUPUESTO_MAXIMO - mejor_resultado_global.get("costo", 0)
    
    return {
        "historial": historial,
        "cromosoma_ganador": mejor_cromosoma_global,
        "acciones_elegidas": mejor_resultado_global.get("acciones", []),
        "inversion": mejor_resultado_global.get("costo", 0),
        "beneficio": mejor_resultado_global.get("beneficio", 0),
        "presupuesto_restante": presupuesto_restante
    }