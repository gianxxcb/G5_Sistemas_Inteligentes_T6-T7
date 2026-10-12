"""Pruebas del evaluador del integrante 2."""

import unittest

from codigo.algoritmo_genetico.busqueda_exhaustiva import buscar_optimo_exacto
from codigo.algoritmo_genetico.evaluacion import ACCIONES, PRESUPUESTO_MAXIMO, evaluar_cromosoma


class PruebaEvaluacion(unittest.TestCase):
    """Verifica costo, beneficio, factibilidad y mejor combinacion exacta."""

    def test_cromosoma_factible(self) -> None:
        cromosoma = (0, 1, 1, 1, 0, 1, 1, 0)
        resultado = evaluar_cromosoma(cromosoma)
        self.assertTrue(resultado["factible"])
        self.assertEqual(resultado["costo"], 19000.0)
        self.assertEqual(resultado["beneficio"], 56.0)
        self.assertEqual(resultado["fitness"], 56.0)

    def test_cromosoma_infactible(self) -> None:
        cromosoma = (1, 1, 1, 1, 1, 1, 1, 1)
        resultado = evaluar_cromosoma(cromosoma)
        self.assertFalse(resultado["factible"])
        self.assertGreater(resultado["costo"], PRESUPUESTO_MAXIMO)
        self.assertLess(resultado["fitness"], 0.0)

    def test_optimo_exacto(self) -> None:
        resultado = buscar_optimo_exacto(len(ACCIONES))
        self.assertEqual(resultado["mejor_cromosoma"], (0, 1, 1, 1, 0, 1, 1, 0))
        self.assertEqual(resultado["optimo"]["beneficio"], 56.0)
        self.assertEqual(resultado["optimo"]["costo"], 19000.0)


if __name__ == "__main__":
    unittest.main()
