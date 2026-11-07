"""Servidor MCP del sistema simulado Centinela."""

import json
from pathlib import Path
from threading import Lock

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from typing_extensions import TypedDict


class Alerta(TypedDict):
    caso_id: str
    nivel: str
    motivo: str
    estado: str


mcp = MCPServer("MCP Detective")
CASOS = json.loads(Path(__file__).with_name("casos.json").read_text(encoding="utf-8"))
alertas: dict[str, Alerta] = {}
bloqueo_alertas = Lock()


def resumir_casos() -> list[dict]:
    return [
        {"caso_id": caso_id, "sistema": caso["sistema"], "cantidad_eventos": len(caso["eventos"])}
        for caso_id, caso in CASOS.items()
    ]


def obtener_eventos(caso_id: str) -> list[dict]:
    if caso_id not in CASOS:
        raise ValueError(f"El caso {caso_id} no existe.")
    return [evento.copy() for evento in CASOS[caso_id]["eventos"]]


def guardar_alerta(caso_id: str, nivel: str, motivo: str) -> Alerta:
    if caso_id not in CASOS:
        raise ValueError(f"El caso {caso_id} no existe.")
    if nivel not in ("bajo", "medio", "alto"):
        raise ValueError("El nivel debe ser bajo, medio o alto.")
    if not isinstance(motivo, str) or not motivo.strip():
        raise ValueError("El motivo debe ser texto y no puede estar vacío.")

    alerta: Alerta = {
        "caso_id": caso_id,
        "nivel": nivel,
        "motivo": motivo,
        "estado": "registrada",
    }
    with bloqueo_alertas:
        if caso_id in alertas:
            raise ValueError(f"Alerta duplicada: el caso {caso_id} ya tiene una alerta.")
        alertas[caso_id] = alerta
    return alerta.copy()


@mcp.tool()
def listar_casos() -> list[dict]:
    """Lista el identificador, el sistema y la cantidad de eventos de cada caso."""
    return resumir_casos()


@mcp.tool()
def consultar_eventos(caso_id: str) -> list[dict]:
    """Devuelve los eventos del caso indicado o informa que el caso no existe."""
    try:
        return obtener_eventos(caso_id)
    except ValueError as error:
        raise ToolError(str(error)) from error


@mcp.tool()
def registrar_alerta(caso_id: str, nivel: str, motivo: str) -> Alerta:
    """Registra en memoria una alerta por caso y devuelve su confirmación."""
    try:
        return guardar_alerta(caso_id, nivel, motivo)
    except ValueError as error:
        raise ToolError(str(error)) from error


if __name__ == "__main__":
    mcp.run(transport="stdio")
