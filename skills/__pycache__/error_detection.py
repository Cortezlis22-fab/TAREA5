
from collections import Counter


def detect_log_errors(report):
    """
    Identifica y organiza los errores encontrados en el reporte.
    """

    errors = [
        event for event in report.events
        if event.severity.value == "ERROR"
    ]

    warnings = [
        event for event in report.events
        if event.severity.value == "WARNING"
    ]

    error_messages = Counter(
        event.message for event in errors
    )

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
