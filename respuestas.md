# MCP Detective — Sebastián Rosero

## 1. Arquitectura

El LLM interpreta los eventos y propone herramientas y argumentos. El host (Codex) coordina la sesión; su cliente MCP descubre las herramientas y envía las llamadas por stdio. El intérprete de Python ejecuta el proceso del servidor MCP: este lee los casos, valida las entradas y registra alertas en memoria. El LLM no ejecuta esas validaciones por sí solo.

## 2. Evidencia

INC-003 contiene cuatro LOGIN_FAILED de admin entre 03:00 y 03:03 y un LOGIN_SUCCESS a las 03:04, todos desde 192.0.2.50 en panel_administracion. El patrón justifica una alerta alta y revisar si el acceso estaba autorizado. Los eventos no identifican a la persona ni prueban una intrusión: también podrían reflejar intentos legítimos con una contraseña equivocada. Esta explicación se apoya en los datos revisados durante la implementación y las pruebas, no se presenta como una investigación completada por un agente en sesión nueva.

## 3. Validación y seguridad

El servidor rechaza casos inexistentes, niveles distintos de bajo/medio/alto, motivos no textuales o en blanco y alertas duplicadas. La lógica utiliza ValueError. En MCP 2.3.0, las tools traducen esas excepciones a ToolError para comunicar su mensaje al cliente. No basta confiar en el modelo: puede producir argumentos incorrectos. El servidor aplica las reglas de forma determinista antes de modificar el estado.

## Instalación e Inspector

Requisitos: Python >=3.11 y Node.js con npx. Desde la raíz:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest mcp-detective -q
mcp dev mcp-detective/server.py
```

En Windows, activar con `.venv\Scripts\Activate.ps1` en PowerShell.

Descubrir las tres tools y ejecutar D1–D7 de la consigna. Para verificar la memoria, repetir una alerta en el mismo proceso (debe fallar), terminar el servidor y el Inspector, volver a ejecutar mcp dev y repetirla (debe funcionar). Una conexión nueva no demuestra por sí sola un reinicio.

## Agente y conexión

Agente de implementación: Codex. Host previsto para la investigación: Codex CLI, en sesión nueva. Registrar el servidor usando rutas absolutas:

```bash
codex mcp add centinela -- /ruta/absoluta/.venv/bin/python /ruta/absoluta/mcp-detective/server.py
```

Después, iniciar una sesión nueva y pedir discovery, listar_casos, consultar_eventos para cada caso, una alerta justificada para INC-003 y consultar_eventos para INC-999. Durante esa investigación queda prohibido leer casos.json directamente. La conexión se debe demostrar con las llamadas MCP, sus argumentos y resultados.

La sesión nueva se intentó durante este trabajo, pero falló por autenticación caducada antes de realizar la investigación. Por tanto, esa conexión y la investigación no se certifican como completadas.

## Verificación y procedencia de imágenes

Se ejecutaron las 9 pruebas del ZIP con el SDK oficial MCP 2.3.0: 9 passed. Posteriormente se probaron mejoras locales con 12 pruebas, D1–D7 en Inspector y un reinicio real; esos cambios y capturas nuevas quedaron en un entorno que perdió conexión. Esta publicación conserva el código y las 9 pruebas del ZIP, no atribuye las 12 pruebas a esta versión.

Las cinco imágenes de evidencias/ se recuperaron sin modificar del ZIP suministrado. Son material de origen, no capturas nuevas certificadas por esta publicación. Las imágenes revisadas del Inspector y del agente presentan resultados recompuestos y no sustituyen las capturas de interfaz exigidas por la consigna. Sigue pendiente sustituirlas por capturas originales verificables y completar la investigación del agente.
