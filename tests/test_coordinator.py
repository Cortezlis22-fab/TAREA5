
from datetime import date
from pathlib import Path
from types import SimpleNamespace

from models import AnalysisReport, LogEvent, Severity
from core.coordinator import LogAnalyzerCoordinator


def create_test_report():
    event = LogEvent(
        line_number=1,
        original_text="[ERROR] 2025-01-10 Error de conexión",
        severity=Severity.ERROR,
        event_date=date(2025, 1, 10),
        message="Error de conexión",
        issues=()
    )

    return AnalysisReport(
        source=Path("test_logs.txt"),
        events=[event],
        ignored_blank_lines=0
    )


def test_coordinator_runs_both_agents():
    report = create_test_report()

    fake_response = SimpleNamespace(
        text="Se detectó un problema de conexión."
    )

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **kwargs: fake_response
        )
    )

    coordinator = LogAnalyzerCoordinator(fake_client)

    result = coordinator.run_analysis(report)

    assert "diagnostic" in result
    assert "ai_report" in result
    assert result["diagnostic"]["errors"]["total_errors"] == 1
    assert result["ai_report"]["ai_analysis"] == (
        "Se detectó un problema de conexión."
    )
