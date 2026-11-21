
def generate_recommendations(error_data, statistics):
    """
    Genera recomendaciones según los errores y estadísticas.
    """

    recommendations = []

    if error_data["total_errors"] > 0:
        recommendations.append(
            "Revisar los errores registrados y determinar su causa."
        )

    if error_data["total_warnings"] > 0:
        recommendations.append(
            "Investigar las advertencias para prevenir problemas futuros."
        )

    if statistics["invalid_events"] > 0:
        recommendations.append(
            "Verificar el formato de los eventos inválidos."
        )

    if statistics["total_events"] == 0:
        recommendations.append(
            "El archivo no contiene eventos para analizar."
        )

    if not recommendations:
        recommendations.append(
            "No se detectaron problemas importantes. "
            "Continuar monitoreando los registros."
        )

    return recommendations
