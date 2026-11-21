
from collections import Counter


def detect_log_errors(report):
    """
    Identifica y organiza los errores encontrados en el reporte.
    """

    # Identificar eventos con severidad ERROR
    errors = [
        event for event in report.events
        if event.severity.value == "ERROR"
    ]

    # Identificar eventos con severidad WARNING
    warnings = [
        event for event in report.events
        if event.severity.value == "WARNING"
    ]

    # Contar los mensajes de error repetidos
    error_messages = Counter(
        event.message for event in errors
    )

    # Organizar los resultados
    return {
        "total_errors": len(errors),
        "total_warnings": len(warnings),
        "error_messages": dict(error_messages),
        "error_details": [
            {
                "line": event.line_number,
                "message": event.message,
                "issues": list(event.issues)
            }
            for event in errors
        ]
    }
