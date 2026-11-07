import pytest

from server import alertas, guardar_alerta, obtener_eventos, resumir_casos


@pytest.fixture(autouse=True)
def aislar_alertas():
    alertas.clear()
    yield
    alertas.clear()


def test_listar_casos():
    assert {caso["caso_id"]: caso["cantidad_eventos"] for caso in resumir_casos()} == {
        "INC-001": 2,
        "INC-002": 6,
        "INC-003": 5,
    }


def test_consultar_caso_desconocido():
    with pytest.raises(ValueError, match="INC-999 no existe"):
        obtener_eventos("INC-999")


def test_consultar_caso_valido():
    eventos = obtener_eventos("INC-002")
    assert len(eventos) == 6
    assert all(e["evento"] == "LOGIN_FAILED" and e["usuario"] == "admin" for e in eventos)


def test_registrar_alerta():
    alerta = guardar_alerta("INC-003", "alto", "Revisar acceso exitoso")
    assert alerta == {
        "caso_id": "INC-003",
        "nivel": "alto",
        "motivo": "Revisar acceso exitoso",
        "estado": "registrada",
    }
    assert alertas["INC-003"] == alerta


def test_rechazar_alerta_duplicada():
    alerta = guardar_alerta("INC-003", "alto", "Revisar acceso exitoso")
    with pytest.raises(ValueError, match="Alerta duplicada"):
        guardar_alerta("INC-003", "medio", "Otro motivo")
    assert alertas["INC-003"] == alerta


@pytest.mark.parametrize(
    ("caso_id", "nivel", "motivo", "mensaje"),
    [
        ("INC-999", "medio", "Revisar", "INC-999 no existe"),
        ("INC-002", "critico", "Revisar", "El nivel debe ser"),
        ("INC-002", "medio", "   ", "El motivo debe ser texto"),
        ("INC-002", "medio", 123, "El motivo debe ser texto"),
    ],
)
def test_rechazar_alerta_invalida(caso_id, nivel, motivo, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        guardar_alerta(caso_id, nivel, motivo)
    assert alertas == {}
