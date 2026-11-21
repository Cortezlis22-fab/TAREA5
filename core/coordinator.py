
from agents.diagnostic_agent import DiagnosticAgent
from agents.report_agent import ReportAgent


class LogAnalyzerCoordinator:
    """
    Coordina los agentes encargados del análisis de logs.
    """

    def __init__(self, gemini_client):
        self.diagnostic_agent = DiagnosticAgent()
        self.report_agent = ReportAgent(gemini_client)

    def run_analysis(self, report):
        # Ejecutar el diagnóstico tradicional
        diagnostic_results = self.diagnostic_agent.analyze(report)

        # Generar el análisis inteligente con Gemini
        ai_results = self.report_agent.generate_report(report)

        # Unificar los resultados
        return {
            "diagnostic": diagnostic_results,
            "ai_report": ai_results
        }
