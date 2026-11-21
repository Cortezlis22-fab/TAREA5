
from skills.error_detection import detect_log_errors
from skills.statistics import generate_log_statistics
from skills.recommendations import generate_recommendations


class DiagnosticAgent:
    """
    Agente encargado de coordinar el diagnóstico de los logs.
    """

    def analyze(self, report):
        # Detectar errores y advertencias
        error_data = detect_log_errors(report)

        # Generar estadísticas
        statistics = generate_log_statistics(report)

        # Crear recomendaciones
        recommendations = generate_recommendations(
            error_data,
            statistics
        )

        # Organizar los resultados
        return {
            "errors": error_data,
            "statistics": statistics,
            "recommendations": recommendations
        }
