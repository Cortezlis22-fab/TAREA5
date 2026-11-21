
from skills.log_analysis import analyze_logs_with_gemini


class ReportAgent:
    """
    Agente encargado de generar informes inteligentes
    utilizando Gemini.
    """

    def __init__(self, client):
        self.client = client

    def generate_report(self, report):
        # Solicitar el análisis inteligente a Gemini
        analysis = analyze_logs_with_gemini(
            report,
            self.client
        )

        return {
            "ai_analysis": analysis
        }
