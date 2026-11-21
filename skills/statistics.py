
from collections import Counter


def generate_log_statistics(report):
    """
    Genera estadísticas generales del archivo de logs.
    """

    severity_counts = Counter(
        event.severity.value for event in report.events
    )

    valid_events = [
        event for event in report.events
        if event.is_valid
    ]

    invalid_events = [
        event for event in report.events
        if not event.is_valid
    ]

    return {
        "total_events": report.total_events,
        "valid_events": len(valid_events),
        "invalid_events": len(invalid_events),
        "ignored_blank_lines": report.ignored_blank_lines,
        "severity_distribution": dict(severity_counts)
    }
