# Deber 5 — MCP Detective

**Sebastián Rosero** · USFQ  
**Materia:** Programación Asistida de Aplicaciones  
**Profesor:** José David Vega Sánchez

Servidor MCP en Python para investigar los incidentes simulados del sistema Centinela.

## Archivos

- [Servidor MCP](mcp-detective/server.py): exactamente tres tools (`listar_casos`, `consultar_eventos`, `registrar_alerta`).
- [Casos](mcp-detective/casos.json): datos del enunciado.
- [Pruebas pytest](mcp-detective/test_server.py): reglas y validaciones.
- [Verificación MCP stdio](mcp-detective/verificar_mcp.py): descubrimiento, D1–D7 y reinicio de memoria.
- [Respuestas](respuestas.md): arquitectura, análisis, seguridad e instrucciones.
- [Evidencias](evidencias/): cinco archivos solicitados.
- [GitHub Actions](.github/workflows/verificacion.yml): ejecuta las pruebas automáticamente.

## Requisitos

Python 3.11 o superior, Node.js y npx (para MCP Inspector).

## Instalación

Desde la raíz del proyecto:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Para activar el entorno, en Windows PowerShell se usa `.venv\Scripts\Activate.ps1`; en Linux/macOS, `source .venv/bin/activate`.

## Pruebas

```bash
python -m pytest mcp-detective -q
python mcp-detective/verificar_mcp.py
```

La primera orden ejecuta las pruebas de lógica. La segunda usa un cliente MCP real sobre `stdio`, comprueba las tres herramientas, verifica D1–D7 y confirma que reiniciar el proceso limpia las alertas en memoria.

También hay ejecuciones automatizadas en [GitHub Actions](../../actions).

## MCP Inspector

```bash
mcp dev mcp-detective/server.py
```

En Inspector se descubren las tres herramientas y se ejecutan D1–D7. La prueba D5 requiere repetir el registro en **el mismo proceso**. Para comprobar el reinicio hay que cerrar el servidor, iniciarlo de nuevo y repetir el registro.

## Investigación desde Codex

Configura el host MCP con la ruta absoluta del intérprete Python y de `mcp-detective/server.py`. Abre una sesión **nueva** para investigar y usa únicamente las herramientas MCP para descubrir los casos y consultar sus eventos. No leas `casos.json` directamente durante esa sesión. La evidencia debe mostrar las llamadas reales con sus argumentos y resultados.

## Entrega

[Pull request #1: `deber5` hacia `main`](../../pull/1). Se conserva abierto para evaluación.