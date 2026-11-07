# Deber 5 — MCP Detective

Sebastián Rosero · USFQ  
Programación Asistida de Aplicaciones  
Profesor: José David Vega Sánchez

El proyecto está extraído en la rama **deber5**:

- [Servidor](mcp-detective/server.py), [casos](mcp-detective/casos.json) y [pruebas](mcp-detective/test_server.py).
- [Respuestas e instrucciones](respuestas.md).
- [Imágenes del ZIP original](evidencias/).

## Ejecutar

Python >=3.11; Node.js y npx para Inspector.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest mcp-detective -q
mcp dev mcp-detective/server.py
```

En Windows, activar con `.venv\Scripts\Activate.ps1`.

## Estado real

Publicación del contenido del ZIP como archivos navegables. Se conservan el servidor, datos, pruebas y las cinco imágenes originales; respuestas.md aclara qué se verificó y qué falta. Las 9 pruebas del ZIP pasaron durante la ejecución previa con MCP 2.3.0. No se volvió a ejecutar el proyecto tras perder el entorno.

Las imágenes originales no se certifican como capturas auténticas de interfaz. Falta completar la investigación en una sesión nueva autenticada del agente y sustituir las evidencias que no cumplen la consigna. El PR no implica cumplimiento completo del deber.

El ZIP original permanece en el historial y en main. La rama deber5 muestra los archivos extraídos.
