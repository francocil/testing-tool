from unittest.mock import patch, MagicMock


def _fake_ejecucion(id=1):
    fake = MagicMock()
    fake.id = id
    fake.caso_id = 10
    fake.usuario_id = 20
    fake.modo = "automatico"
    fake.estado = "en_progreso"
    fake.resultado_global = None
    fake.porcentaje_aceptacion = None
    fake.fecha = "2025-01-01T00:00:00"
    fake.fecha_fin = None
    fake.pasos = []
    return fake


# ============================================================
# /{id}/siguiente-paso
# ============================================================

@patch("routes.ejecucion.ejecutar_siguiente_paso")
def test_siguiente_paso(mock_motor, client):
    mock_motor.return_value = _fake_ejecucion(1)

    resp = client.post("/api/v1/ejecuciones/1/siguiente-paso")
    assert resp.status_code == 200

    mock_motor.assert_called_once()
    args, kwargs = mock_motor.call_args
    assert args[1] == 1

    data = resp.json()
    assert data["id"] == 1


# ============================================================
# /{id}/ejecutar
# ============================================================

@patch("routes.ejecucion.ejecutar_ejecucion")
def test_ejecutar(mock_motor, client):
    mock_motor.return_value = _fake_ejecucion(2)

    resp = client.post("/api/v1/ejecuciones/2/ejecutar")
    assert resp.status_code == 200

    mock_motor.assert_called_once()
    args, kwargs = mock_motor.call_args
    assert args[1] == 2

    data = resp.json()
    assert data["id"] == 2


# ============================================================
# /{id}/pasos/{paso_id}/manual
# ============================================================

@patch("routes.ejecucion.get_ejecucion")
@patch("routes.ejecucion.registrar_paso_manual")
def test_manual(mock_registrar, mock_get, client):
    mock_get.return_value = _fake_ejecucion(3)

    resp = client.post(
        "/api/v1/ejecuciones/3/pasos/5/manual",
        params={"estado": "ok", "resultado": "Todo bien"}
    )
    assert resp.status_code == 200

    mock_registrar.assert_called_once()
    args, kwargs = mock_registrar.call_args
    assert args[1] == 3
    assert args[2] == 5
    assert args[3] == "ok"
    assert args[4] == "Todo bien"

    data = resp.json()
    assert data["id"] == 3
