"""Componentes del sistema de urgencia de recoleccion basado en logica difusa."""

from .inferencia_mamdani import ResultadoUrgencia, evaluar_urgencia

__all__ = ["ResultadoUrgencia", "evaluar_urgencia"]
