
from datetime import date
from pathlib import Path
from types import SimpleNamespace

from models import AnalysisReport, LogEvent, Severity

from skills.log_analysis import analyze_logs_with_gemini
from skills.error_detection import detect_log_errors
from skills.statistics import generate_log_statistics
from skills.recommendations import generate_recommendations


def create_test_report():
    """Crea un reporte ficticio para probar las skills."""

    events = [
        LogEvent(
            line_number=1,
            original_text="[INFO] 2025-01-10 Sistema iniciado",
            severity=Severity.INFO,
            event_date=date(2025, 1, 10),
            message="Sistema iniciado",
            issues=()
        ),
        LogEvent(
            line_number=2,
            original_text="[WARNING] 2025-01-11 Memoria casi llena",
            severity=Severity.WARNING,
            event_date=date(2025, 1, 11),
            message="Memoria casi llena",
            issues=()
        ),
        LogEvent(
            line_number=3,
            original_text="[ERROR] 2025-01-12 Error de conexión",
            severity=Severity.ERROR,
            event_date=date(2025, 1, 12),
            message="Error de conexión",
            issues=()
        )
    ]

    return AnalysisReport(
        source=Path("test_logs.txt"),
        events=events,
        ignored_blank_lines=0
    )


def test_error_detection():
    report = create_test_report()

    result = detect_log_errors(report)

    assert result["total_errors"] == 1
    assert result["total_warnings"] == 1
    assert "Error de conexión" in result["error_messages"]


def test_statistics():
    report = create_test_report()

    result = generate_log_statistics(report)

    assert result["total_events"] == 3
    assert result["valid_events"] == 3
    assert result["invalid_events"] == 0
    assert result["severity_distribution"]["INFO"] == 1


def test_recommendations():
    report = create_test_report()

    errors = detect_log_errors(report)
    statistics = generate_log_statistics(report)

    result = generate_recommendations(errors, statistics)

    assert len(result) > 0
    assert any("errores" in item.lower() for item in result)


def test_log_analysis_with_gemini():
    report = create_test_report()

    # Simular una respuesta de Gemini sin consumir API
    fake_response = SimpleNamespace(
        text="Se detectó un error de conexión."
    )

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **kwargs: fake_response
        )
    )

    result = analyze_logs_with_gemini(report, fake_client)

    assert result == "Se detectó un error de conexión."
