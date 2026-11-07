#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p inspector-resultados
INSPECTOR=(npx -y @modelcontextprotocol/inspector --cli python mcp-detective/server.py)

echo "Inspector CLI: Discovery"
"${INSPECTOR[@]}" --method tools/list --format json > inspector-resultados/tools.json
echo "Inspector CLI: D1 listar_casos"
"${INSPECTOR[@]}" --method tools/call --tool-name listar_casos --format json > inspector-resultados/d1.json
echo "Inspector CLI: D2 consultar_eventos INC-002"
"${INSPECTOR[@]}" --method tools/call --tool-name consultar_eventos --tool-args-json '{"caso_id":"INC-002"}' --format json > inspector-resultados/d2.json

esperar_error() {
    local nombre="$1"
    shift
    echo "Inspector CLI: $nombre (error esperado)"
    if "${INSPECTOR[@]}" --method tools/call "$@" --format json > "inspector-resultados/${nombre}.json"; then
        echo "$nombre: el Inspector no rechazó una llamada inválida" >&2
        exit 1
    else
        local codigo=$?
        if [ "$codigo" -ne 5 ]; then
            echo "$nombre: código de salida inesperado $codigo" >&2
            exit 1
        fi
    fi
}
esperar_error d3 --tool-name consultar_eventos --tool-args-json '{"caso_id":"INC-999"}'
echo "Inspector CLI: D4 registrar_alerta válida"
"${INSPECTOR[@]}" --method tools/call --tool-name registrar_alerta --tool-args-json '{"caso_id":"INC-003","nivel":"alto","motivo":"Cuatro fallos y un acceso exitoso; requiere investigación"}' --format json > inspector-resultados/d4.json
# D5 se prueba por MCP Client en el mismo proceso; este CLI lanza procesos individuales.
esperar_error d6 --tool-name registrar_alerta --tool-args-json '{"caso_id":"INC-002","nivel":"critico","motivo":"Intentos repetidos"}'
esperar_error d7 --tool-name registrar_alerta --tool-args-json '{"caso_id":"INC-002","nivel":"medio","motivo":"   "}'
python - <<'PY'
import json
from pathlib import Path
r = Path("inspector-resultados")
leer = lambda nombre: json.loads((r / f"{nombre}.json").read_text(encoding="utf-8"))
tools = leer("tools")["result"]["tools"]
assert {t["name"] for t in tools} == {"listar_casos", "consultar_eventos", "registrar_alerta"}
for caso in ("INC-001", "INC-002", "INC-003"):
    assert caso in json.dumps(leer("d1"), ensure_ascii=False)
assert json.dumps(leer("d2"), ensure_ascii=False).count("LOGIN_FAILED") >= 6
assert "registrada" in json.dumps(leer("d4"), ensure_ascii=False)
for nombre in ("d3", "d6", "d7"):
    assert leer(nombre)["result"]["isError"] is True, nombre
print("Inspector CLI: discovery, D1, D2, D3, D4, D6 y D7 comprobados correctamente")
print("D5 y reinicio: verificar_mcp.py")
PY
