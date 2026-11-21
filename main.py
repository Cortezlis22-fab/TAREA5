import sys
import os
from collections import Counter
from pathlib import Path
from tkinter import Tk, filedialog

from dotenv import load_dotenv
from google import genai

from analyzer import LogAnalyzer
from models import AnalysisReport, Severity
from core.coordinator import LogAnalyzerCoordinator

def select_file() -> Path | None:
    """Permite al usuario seleccionar un archivo de texto."""

    # Crear una ventana de Tkinter sin mostrar la ventana principal.
    root = Tk()
    root.withdraw()

    # Mantener el selector de archivos visible sobre otras ventanas.
    root.attributes("-topmost", True)

    try:
        # Mostrar el cuadro de diálogo para seleccionar un archivo TXT.
        selected_file = filedialog.askopenfilename(
            title="Seleccionar archivo de logs",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        # Convertir la ruta seleccionada en un objeto Path.
        # Si el usuario cancela, devolver None.
        return Path(selected_file) if selected_file else None

    finally:
        # Cerrar la ventana de Tkinter incluso si ocurre un error.
        root.destroy()


def print_report(report: AnalysisReport) -> None:
    """Muestra las estadísticas del análisis en consola."""

    # Contabilizar cuántos eventos pertenecen a cada nivel de severidad.
    severity_counts = Counter(
        event.severity for event in report.events
    )

    print("\n" + "=" * 55)
    print("             REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 55)

    print(f"\nArchivo analizado: {report.source}")
    print(f"Total de eventos: {report.total_events}")

    # Mostrar la cantidad de eventos correspondientes a cada severidad.
    print("\nEVENTOS POR SEVERIDAD")
    print("-" * 35)

    for severity in Severity:
        count = severity_counts.get(severity, 0)
        print(f"{severity.value:<12}: {count}")

    # Presentar el estado general de los registros analizados.
    print("\nESTADO DE LOS REGISTROS")
    print("-" * 35)

    # Los registros válidos se obtienen restando los malformados del total.
    print(
        f"Registros válidos: "
        f"{report.total_events - len(report.malformed_events)}"
    )

    print(
        f"Registros malformados: "
        f"{len(report.malformed_events)}"
    )

    # Las líneas vacías se contabilizan aparte y no forman parte de los eventos.
    print(
        f"Líneas vacías ignoradas: "
        f"{report.ignored_blank_lines}"
    )

    # Mostrar los detalles de los registros que contienen problemas.
    if report.malformed_events:
        print("\nDETALLE DE REGISTROS INCORRECTOS")
        print("-" * 35)

        for event in report.malformed_events:
            print(
                f"\nLínea {event.line_number}: "
                f"{event.original_text}"
            )

            # Un registro puede presentar uno o varios problemas.
            for issue in event.issues:
                print(f"  - {issue}")

    print("\n" + "=" * 55)
    print("          ANÁLISIS FINALIZADO")
    print("=" * 55)


def main() -> int:
    """Coordina el análisis tradicional y el análisis inteligente."""

    print("\nANALIZADOR INTELIGENTE DE ARCHIVOS DE LOGS")
    print("Selecciona un archivo TXT para comenzar.\n")

    client = None

    try:
        # Cargar la API key desde el archivo .env
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("Error: no se encontró la API key de Gemini.")
            return 1

        # Seleccionar el archivo
        file_path = select_file()

        if file_path is None:
            print("Operación cancelada: no se seleccionó un archivo.")
            return 0

        # Ejecutar el analizador original
        analyzer = LogAnalyzer()
        report = analyzer.analyze(file_path)

        # Crear el cliente de Gemini
        client = genai.Client(api_key=api_key)

        # Crear el coordinador de agentes
        coordinator = LogAnalyzerCoordinator(client)

        # Ejecutar el análisis completo
        results = coordinator.run_analysis(report)

        # Mostrar el reporte original
        print_report(report)

        # Mostrar el diagnóstico de Python
        diagnostic = results["diagnostic"]

        print("\nDIAGNÓSTICO INTELIGENTE")
        print("=" * 55)

        print("\nErrores:", diagnostic["errors"]["total_errors"])
        print("Advertencias:", diagnostic["errors"]["total_warnings"])

        print("\nESTADÍSTICAS")
        print(diagnostic["statistics"])

        print("\nRECOMENDACIONES")
        for recommendation in diagnostic["recommendations"]:
            print("-", recommendation)

        # Mostrar el análisis generado por Gemini
        print("\nANÁLISIS GENERADO POR GEMINI")
        print("=" * 55)
        print(results["ai_report"]["ai_analysis"])

        return 0

    except PermissionError:
        print("Error: no tienes permisos para leer el archivo.")
        return 1

    except UnicodeError:
        print("Error: no fue posible interpretar el archivo.")
        return 1

    except OSError as error:
        print(f"Error de lectura: {error}")
        return 1

    except Exception as error:
        print(f"Error inesperado: {type(error).__name__}: {error}")
        return 1

    finally:
        if client is not None:
            client.close()

if __name__ == "__main__":
    # Ejecutar el programa principal
    sys.exit(main())
