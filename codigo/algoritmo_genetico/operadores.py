import random

def generar_poblacion(tamano_poblacion, longitud_cromosoma, semilla=None):
    if semilla is not None:
        random.seed(semilla)
    poblacion = []
    for _ in range(tamano_poblacion):
        individuo = [random.choice([0, 1]) for _ in range(longitud_cromosoma)]
        poblacion.append(individuo)
    return poblacion

def seleccion_torneo(poblacion, lista_fitness, tamano_torneo):
    indices = list(range(len(poblacion)))
    seleccionados_torneo = random.sample(indices, tamano_torneo)
    mejor_indice = max(seleccionados_torneo, key=lambda i: lista_fitness[i])
    return poblacion[mejor_indice]

def cruce_un_punto(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

def mutacion_inversion_bits(cromosoma, tasa_mutacion):
    cromosoma_mutado = []
    for gen in cromosoma:
        if random.random() < tasa_mutacion:
            cromosoma_mutado.append(1 - gen)
        else:
            cromosoma_mutado.append(gen)
    return cromosoma_mutado

def aplicar_elitismo(poblacion, lista_fitness):
    mejor_indice = lista_fitness.index(max(lista_fitness))
    return poblacion[mejor_indice]