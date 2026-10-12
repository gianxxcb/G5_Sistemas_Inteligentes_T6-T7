from codigo.algoritmo_genetico.operadores import generar_poblacion
from codigo.algoritmo_genetico.algoritmo import ejecutar_algoritmo_genetico
from unittest.mock import patch


def test_longitud_y_valores_binarios():
    """Verifica que los cromosomas tengan 8 genes y sean exclusivamente binarios."""
    poblacion = generar_poblacion(tamano_poblacion=10, longitud_cromosoma=8, semilla=42)
    
    assert len(poblacion) == 10
    for individuo in poblacion:
        assert len(individuo) == 8, "El cromosoma debe tener exactamente 8 genes."
        for gen in individuo:
            assert gen in (0, 1), "Cada gen debe ser un valor binario (0 o 1)."


def test_reproducibilidad_semilla():
    """Garantiza que ejecuciones con la misma semilla entreguen exactamente el mismo resultado."""
    configuracion = {
        "tamano_poblacion": 10,
        "num_generaciones": 5,
        "tasa_mutacion": 0.1,
        "tamano_torneo": 2,
    }
    
    resultado1 = ejecutar_algoritmo_genetico(configuracion, semilla=11)
    resultado2 = ejecutar_algoritmo_genetico(configuracion, semilla=11)

    assert resultado1["cromosoma_ganador"] == resultado2["cromosoma_ganador"]
    assert resultado1["inversion"] == resultado2["inversion"]
    assert resultado1["beneficio"] == resultado2["beneficio"]


def test_probabilidad_cruce_cero_omite_el_operador():
    configuracion = {
        "tamano_poblacion": 10,
        "num_generaciones": 3,
        "tasa_mutacion": 0.0,
        "probabilidad_cruce": 0.0,
        "tamano_torneo": 2,
    }

    with patch("codigo.algoritmo_genetico.algoritmo.cruce_un_punto") as cruce:
        ejecutar_algoritmo_genetico(configuracion, semilla=11)

    cruce.assert_not_called()


if __name__ == "__main__":
    test_longitud_y_valores_binarios()
    test_reproducibilidad_semilla()
    print("Pruebas unitarias completadas exitosamente.")