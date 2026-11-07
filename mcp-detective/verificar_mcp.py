"""Verificaciones reproducibles de MCP por transporte stdio, sin usar un LLM.

Ejecutar: python mcp-detective/verificar_mcp.py
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import Client, StdioServerParameters

SERVER = Path(__file__).with_name("server.py").resolve()


def contenido(resultado: Any) -> Any:
    """Extrae el contenido de una respuesta MCP en formato Python."""
    data = getattr(resultado, "structured_content", None)
    if data is not None:
        return data.get("result", data) if isinstance(data, dict) else data
    texto = "\n".join(
        getattr(parte, "text", "") for parte in resultado.content
        if getattr(parte, "text", None)
    )
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return texto


def asegurar(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise AssertionError(mensaje)


async def comprobar_error(cliente: Client, herramienta: str, args: dict, descripcion: str) -> None:
    resultado = await cliente.call_tool(herramienta, args)
    asegurar(resultado.is_error is True, f"{descripcion}: debería fallar por MCP")
    texto = " ".join(getattr(c, "text", "") for c in resultado.content)
    asegurar(bool(texto.strip()), f"{descripcion}: el error no tiene mensaje")
    print(f"{descripcion}: OK — {texto.strip()}")


async def main() -> None:
    parametros = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with Client(parametros) as cliente:
        herramientas = await cliente.list_tools()
        nombres = {herramienta.name for herramienta in herramientas.tools}
        asegurar(nombres == {"listar_casos", "consultar_eventos", "registrar_alerta"},
                f"Discovery incorrecto: {nombres}")
        print("Discovery: OK — exactamente tres tools MCP")

        resultado = await cliente.call_tool("listar_casos", {})
        asegurar(not resultado.is_error, "D1: error inesperado")
        datos = contenido(resultado)
        asegurar({d["caso_id"]: d["cantidad_eventos"] for d in datos} ==
                {"INC-001": 2, "INC-002": 6, "INC-003": 5}, "D1: datos incorrectos")
        print("D1: OK — tres casos y cantidades exactas")

        resultado = await cliente.call_tool("consultar_eventos", {"caso_id": "INC-002"})
        asegurar(not resultado.is_error, "D2: error inesperado")
        eventos = contenido(resultado)
        asegurar(len(eventos) == 6 and
                all(e["usuario"] == "admin" and e["evento"] == "LOGIN_FAILED" for e in eventos),
                "D2: registros incorrectos")
        print("D2: OK — seis intentos fallidos")

        await comprobar_error(cliente, "consultar_eventos", {"caso_id": "INC-999"}, "D3")

        motivo = "Cuatro fallos y un acceso exitoso desde la misma IP; requiere investigación"
        args = {"caso_id": "INC-003", "nivel": "alto", "motivo": motivo}
        resultado = await cliente.call_tool("registrar_alerta", args)
        asegurar(not resultado.is_error, "D4: error inesperado")
        alerta = contenido(resultado)
        asegurar(all(alerta.get(k) == v for k, v in {**args, "estado": "registrada"}.items()),
                f"D4: confirmación incorrecta: {alerta}")
        print("D4: OK — alerta registrada")

        await comprobar_error(cliente, "registrar_alerta", args, "D5")
        await comprobar_error(cliente, "registrar_alerta", {
            "caso_id": "INC-002", "nivel": "critico", "motivo": "Intentos repetidos"}, "D6")
        await comprobar_error(cliente, "registrar_alerta", {
            "caso_id": "INC-002", "nivel": "medio", "motivo": "   "}, "D7")

    # Un nuevo Client con stdio inicia un nuevo proceso del servidor.
    async with Client(parametros) as cliente:
        resultado = await cliente.call_tool("registrar_alerta", args)
        asegurar(not resultado.is_error, "Reinicio: no se limpió la memoria")
        asegurar(contenido(resultado).get("estado") == "registrada",
                "Reinicio: confirmación incorrecta")
        print("Reinicio: OK — memoria reiniciada")

    print("Todas las comprobaciones MCP stdio han pasado.")


if __name__ == "__main__":
    asyncio.run(main())
