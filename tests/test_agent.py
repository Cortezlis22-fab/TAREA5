
from datetime import date
from pathlib import Path
from types import SimpleNamespace

from models import AnalysisReport, LogEvent, Severity
from agents.diagnostic_agent import DiagnosticAgent
from agents.report_agent import ReportAgent


def create_test_report():
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
            original_text="[ERROR] 2025-01-11 Error de conexión",
            severity=Severity.ERROR,
            event_date=date(2025, 1, 11),
            message="Error de conexión",
            issues=()
        )
    ]

    return AnalysisReport(
        source=Path("test_logs.txt"),
        events=events,
        ignored_blank_lines=0
    )


def test_diagnostic_agent():
    report = create_test_report()

    agent = DiagnosticAgent()
    result = agent.analyze(report)

    assert result["errors"]["total_errors"] == 1
    assert result["statistics"]["total_events"] == 2
    assert len(result["recommendations"]) > 0


def test_report_agent():
    report = create_test_report()

    fake_response = SimpleNamespace(
        text="Se detectó un error de conexión."
    )

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **kwargs: fake_response
        )
    )

    agent = ReportAgent(fake_client)
    result = agent.generate_report(report)

    assert result["ai_analysis"] == "Se detectó un error de conexión."
