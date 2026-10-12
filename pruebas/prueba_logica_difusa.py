"""Pruebas basicas del motor difuso implementado por el integrante 1."""

import unittest

import numpy as np

from codigo.logica_difusa.funciones_pertenencia import triangular
from codigo.logica_difusa.inferencia_mamdani import evaluar_urgencia
from codigo.logica_difusa.reglas import crear_reglas_urgencia


class PruebasLogicaDifusa(unittest.TestCase):
    """Comprueba propiedades esenciales antes de integrar el resto del proyecto."""

    def test_base_contiene_todas_las_combinaciones(self) -> None:
        self.assertEqual(len(crear_reglas_urgencia()), 27)

    def test_funcion_triangular_alcanza_su_pico(self) -> None:
        universo = np.array([0.0, 5.0, 10.0])
        pertenencia = triangular(universo, 0.0, 5.0, 10.0)
        self.assertEqual(pertenencia.tolist(), [0.0, 1.0, 0.0])

    def test_urgencia_pertenece_al_rango_permitido(self) -> None:
        resultado = evaluar_urgencia(95, 8, 90)
        self.assertGreaterEqual(resultado.valor_urgencia, 0.0)
        self.assertLessEqual(resultado.valor_urgencia, 100.0)
        self.assertGreater(len(resultado.reglas_activadas), 0)


if __name__ == "__main__":
    unittest.main()
