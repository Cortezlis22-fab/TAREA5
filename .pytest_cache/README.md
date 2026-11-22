# LogAnalyzerAI – Analizador Inteligente de Archivos de Logs

## 1. Descripción del proyecto

LogAnalyzerAI es una aplicación desarrollada en Python que permite analizar archivos de logs e identificar errores, advertencias, estadísticas y posibles problemas. Integra Gemini para generar interpretaciones inteligentes y recomendaciones técnicas.

## 2. Tecnologías utilizadas

- Python 3.15.2
- Google Gemini API
- Google Gen AI SDK
- python-dotenv
- Pytest
- Tkinter

## 3. Arquitectura del proyecto

El proyecto utiliza una arquitectura modular organizada en tres componentes principales:

### Skills

- `log_analysis.py`: utiliza Gemini para interpretar los registros.
- `error_detection.py`: identifica errores y advertencias.
- `statistics.py`: genera estadísticas de los eventos.
- `recommendations.py`: genera recomendaciones según los resultados.

### Agents

- `diagnostic_agent.py`: coordina las habilidades de detección, estadísticas y recomendaciones.
- `report_agent.py`: utiliza Gemini para generar el análisis inteligente.

### Core

- `coordinator.py`: coordina ambos agentes y reúne sus resultados.

## 4. Funcionamiento

1. El usuario selecciona un archivo TXT.
2. El analizador procesa los registros.
3. El Diagnostic Agent ejecuta las skills de análisis tradicional.
4. El Report Agent envía la información a Gemini.
5. El coordinador reúne los resultados.
6. La aplicación presenta el diagnóstico y el análisis inteligente.

## 5. Instalación

Instalar las dependencias:

```bash
python -m pip install google-genai python-dotenv pytest
```

Crear un archivo `.env` en la raíz:

```env
GEMINI_API_KEY=tu_clave_api
```

No compartir ni publicar este archivo.

## 6. Ejecución

```bash
python main.py
```

Seleccionar un archivo TXT para comenzar el análisis.

## 7. Pruebas

Ejecutar todas las pruebas automatizadas:

```bash
python -m pytest -v
```

En la versión desarrollada se verificaron 19 pruebas automatizadas aprobadas.

## 8. Seguridad

La API key se almacena mediante variables de entorno y el archivo `.env` está excluido de Git mediante `.gitignore`.

## 9. Estructura principal

- `agents/`
- `skills/`
- `core/`
- `tests/`
- `main.py`
- `analyzer.py`
- `log_parser.py`
- `models.py`
