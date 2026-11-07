# Deber 5 — MCP Detective

**Estudiante:** Sebastián Rosero  
**Materia:** Programación Asistida de Aplicaciones · USFQ

## 1. Arquitectura

El LLM analiza lo que recibe y decide qué herramienta MCP necesita utilizar. El host o harness (en este caso, Codex para la implementación) mantiene la conversación y coordina las acciones. El cliente MCP descubre las herramientas, envía argumentos por `stdio` y entrega las respuestas al host. El servidor MCP es el proceso de **Python** que realmente consulta los casos, valida las entradas y guarda las alertas en memoria. El modelo propone acciones, pero no reemplaza la ejecución ni las validaciones del servidor.

## 2. Evidencia

En `INC-003` aparecen cuatro intentos fallidos de `admin` a las 03:00, 03:01, 03:02 y 03:03, seguidos por un inicio de sesión exitoso a las 03:04. Todos corresponden a la IP `192.0.2.50` y al `panel_administracion`. Vale la pena investigar quién inició la sesión y si estaba autorizado. Aun así, no alcanza para afirmar que hubo una intrusión: también podría ser una persona autorizada que se equivocó varias veces al escribir su contraseña.

## 3. Validación y seguridad

Las entradas inválidas las rechaza el **servidor MCP**. Primero, la lógica Python usa `ValueError` cuando no existe el caso, el nivel está fuera de `bajo`/`medio`/`alto`, el motivo está vacío o la alerta ya existe. Las tools traducen esos errores a `ToolError` para que el cliente y el agente reciban un fallo claro. No es suficiente confiar en el LLM: puede escribir un identificador inexistente o argumentos incorrectos. La validación tiene que funcionar aunque el modelo se equivoque.

## Agente utilizado

Se utilizó **Codex** para la implementación del proyecto. La comunicación real con el servidor se comprobó de manera reproducible mediante un cliente MCP por `stdio` en `mcp-detective/verificar_mcp.py` y con MCP Inspector CLI en `mcp-detective/verificar_inspector.sh`. Esta prueba descubre las tres tools, ejecuta D1–D7 en un mismo proceso cuando corresponde y verifica el reinicio de memoria. No equivale a la investigación de los incidentes con un LLM: para demostrar esa parte, se requiere una sesión nueva del agente y su traza visible de llamadas MCP.

## Instalación y pruebas

Requisitos: Python 3.11 o superior, Node.js y `npx` para Inspector. Desde la raíz del repositorio:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m pytest mcp-detective -q
python mcp-detective/verificar_mcp.py
mcp dev mcp-detective/server.py
```

En Windows PowerShell, para activar el entorno se usa `.venv\Scripts\Activate.ps1`; en Linux/macOS, `source .venv/bin/activate`. `mcp dev` abre Inspector, donde pueden descubrirse y ejecutarse las herramientas. Para probar alertas duplicadas, repetir la misma llamada dentro del proceso; para probar el reinicio, detener el servidor, iniciarlo otra vez y volver a registrar la alerta.

## Conectar el servidor a Codex

La ruta del servidor y la del intérprete Python deben ser absolutas. En Linux/macOS, desde la raíz del repositorio, un ejemplo es:

```bash
codex mcp add centinela -- "$(pwd)/.venv/bin/python" "$(pwd)/mcp-detective/server.py"
```

En Windows, utilizar las rutas absolutas equivalentes de `.venv\Scripts\python.exe` y `mcp-detective\server.py`. Abrir una **conversación nueva** del agente, descubrir las tools MCP y pedirle que liste los casos, consulte los eventos de los tres incidentes, registre una alerta justificada para `INC-003` y consulte `INC-999`. Durante esa investigación no se debe leer `casos.json` por ningún otro medio.

## Resultados reproducibles

El flujo de [GitHub Actions](https://github.com/SebastianRKN/Deber-5-mcp/actions) ejecutó con Python 3.12 el proyecto publicado: **9 pruebas pytest aprobadas**, **D1–D7 aprobados mediante cliente MCP real por stdio** y **reinicio de memoria aprobado**. El SDK MCP por `stdio` aprobó el discovery, D1–D7 y el reinicio. MCP Inspector CLI verificó discovery, D1, D2, D3, D4, D6 y D7; D5, que requiere conservar el mismo proceso, quedó verificado por el cliente MCP. La ejecución y los resultados JSON de Inspector están disponibles en [GitHub Actions](https://github.com/SebastianRKN/Deber-5-mcp/actions/runs/42336500738). Los archivos de evidencia están en `evidencias/`. Para cumplir la parte de investigación con un agente, la captura correspondiente debe mostrar llamadas reales con sus argumentos y resultados.