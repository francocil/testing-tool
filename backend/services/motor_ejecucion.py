# ============================================================
#  MOTOR DE EJECUCIÓN HÍBRIDO (VERSIÓN FINAL)
# ------------------------------------------------------------
#  Ejecuta casos de prueba paso a paso, soportando:
#   - Ejecución automática real (HTTP)
#   - Ejecución automática simulada
#   - Ejecución manual
#   - Modos: automatico, paso_a_paso, mixto
#   - joinedload para evitar N+1 queries
#   - Soporte para parámetros tipo path
#   - Validación JSONPath real
#   - Contexto persistente entre pasos
#   - Manejo robusto de errores
#   - valor_obtenido garantizado como string (nunca None)
#   - Aserciones avanzadas por tipo y operador
#   - Snapshots de parámetros y asserts por paso
# ============================================================

import httpx
import json
import re
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from jsonpath_ng import parse

from models.ejecucion import Ejecucion
from models.ejecucion_paso import EjecucionPaso
from models.paso import Paso
from models.objeto_parametro import ObjetoParametro

from typing import Any


# ============================================================
# UTILIDADES
# ============================================================

def reemplazar_variables(texto: str | None, contexto: dict) -> str | None:
    """
    Reemplaza variables {{var}} usando el contexto acumulado.
    Si el texto es None o vacío, se devuelve tal cual.
    """
    if not texto:
        return texto

    matches = re.findall(r"\{\{(.*?)\}\}", texto)
    for m in matches:
        if m in contexto:
            texto = texto.replace(f"{{{{{m}}}}}", str(contexto[m]))
    return texto


def _get_ejecucion_or_404(db: Session, ejecucion_id: int) -> Ejecucion:
    """
    Obtiene una ejecución con carga anticipada de pasos, caso y parámetros.
    Esto evita N+1 queries y asegura que el motor tenga toda la información.
    """
    ejecucion = (
        db.query(Ejecucion)
        .options(
            joinedload(Ejecucion.pasos)
            .joinedload(EjecucionPaso.paso)
            .joinedload(Paso.parametros)
            .joinedload(ObjetoParametro.api),
            joinedload(Ejecucion.caso),
        )
        .filter(Ejecucion.id == ejecucion_id)
        .first()
    )

    if not ejecucion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejecución no encontrada",
        )

    return ejecucion


# ============================================================
# ASSERTS AVANZADOS
# ============================================================

def _normalizar_operador(op: str) -> str:
    """
    Normaliza operadores legacy a los nuevos.
    """
    mapping = {
        "==": "equals",
        "!=": "not_equals",
        ">": "gt",
        "<": "lt",
        ">=": "gte",
        "<=": "lte",
    }
    return mapping.get(op, op)


def _evaluar_asserts(ejec_paso: EjecucionPaso, paso: Paso, contexto: dict) -> bool:
    """
    Evalúa los asserts asociados al paso usando el JSON de respuesta
    guardado en ejec_paso.response_json / valor_obtenido.

    Si algún assert falla o hay error en su evaluación:
      - marca ejec_paso.tipo_resultado = "fallo_assert" (si venía ok/simulado/manual_ok)
        o "error_tecnico" si es un problema de evaluación
      - agrega el mensaje al valor_obtenido
      - devuelve False

    Si todos pasan, devuelve True.
    """
    asserts = getattr(paso, "asserts", None)
    if not asserts:
        return True

    # Intentamos usar response_json si existe; si no, parseamos valor_obtenido
    response_json = ejec_paso.response_json or {}
    body = ""
    status_code = None
    headers = {}

    if response_json:
        status_code = response_json.get("status_code")
        body = response_json.get("body") or ""
        headers = response_json.get("headers") or {}
        json_body = response_json.get("json") or {}
    else:
        raw = ejec_paso.valor_obtenido or ""
        json_body = {}
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                resp = parsed.get("response", {})
                json_body = resp.get("json", {}) or {}
                body = resp.get("body", "") or ""
                status_code = resp.get("status_code", None)
                headers = resp.get("headers", {}) or {}
        except Exception:
            json_body = {}
            body = ""
            status_code = None
            headers = {}

    for a in asserts:
        tipo = getattr(a, "tipo", None) or ""
        op_raw = getattr(a, "operador", None) or ""
        op = _normalizar_operador(op_raw)
        expr_text = getattr(a, "expresion", None)
        esperado = getattr(a, "valor_esperado", None)
        valor = None

        try:
            # -------------------------
            # Selección de valor según tipo
            # -------------------------
            if tipo == "status_code":
                valor = status_code

            elif tipo == "jsonpath":
                if not expr_text:
                    raise ValueError("Expresión JSONPath requerida para tipo jsonpath")
                expr = parse(expr_text)
                matches = [m.value for m in expr.find(json_body or {})]
                valor = matches[0] if matches else None

            elif tipo == "header":
                if not expr_text:
                    raise ValueError("Nombre de header requerido para tipo header")
                valor = headers.get(expr_text)

            elif tipo == "body_contains":
                valor = body

            elif tipo == "regex":
                valor = body

            elif tipo == "length":
                if expr_text:
                    expr = parse(expr_text)
                    matches = [m.value for m in expr.find(json_body or {})]
                    valor = len(matches)
                else:
                    valor = len(body or "")

            else:
                ejec_paso.tipo_resultado = "error_tecnico"
                ejec_paso.valor_obtenido = (ejec_paso.valor_obtenido or "") + \
                    f"\nASSERT ERROR: tipo de assert desconocido {tipo}"
                return False

            ok = False

            # -------------------------
            # Operadores
            # -------------------------
            if op in ("gt", "lt", "gte", "lte"):
                if valor is None or esperado is None:
                    raise ValueError(
                        f"valor o esperado nulos para comparación numérica (valor={valor}, esperado={esperado})"
                    )
                try:
                    v1 = float(valor)
                    v2 = float(esperado)
                except Exception:
                    raise ValueError(
                        f"no se puede convertir a número (valor={valor}, esperado={esperado})"
                    )

                if op == "gt":
                    ok = v1 > v2
                elif op == "lt":
                    ok = v1 < v2
                elif op == "gte":
                    ok = v1 >= v2
                elif op == "lte":
                    ok = v1 <= v2

            elif op == "equals":
                ok = str(valor) == str(esperado)
            elif op == "not_equals":
                ok = str(valor) != str(esperado)
            elif op == "contains":
                ok = str(esperado) in str(valor)
            elif op == "not_contains":
                ok = str(esperado) not in str(valor)

            elif op == "matches_regex":
                if esperado is None:
                    raise ValueError("valor_esperado requerido para matches_regex")
                pattern = re.compile(esperado)
                ok = bool(pattern.search(str(valor)))

            elif op in ("len_equals", "len_gt", "len_lt"):
                if valor is None:
                    length = 0
                elif isinstance(valor, (list, dict, set, tuple)):
                    length = len(valor)
                else:
                    length = len(str(valor))

                try:
                    esperado_len = int(esperado) if esperado is not None else 0
                except Exception:
                    raise ValueError("valor_esperado debe ser entero para operadores de longitud")

                if op == "len_equals":
                    ok = length == esperado_len
                elif op == "len_gt":
                    ok = length > esperado_len
                elif op == "len_lt":
                    ok = length < esperado_len

            else:
                ejec_paso.tipo_resultado = "error_tecnico"
                ejec_paso.valor_obtenido = (ejec_paso.valor_obtenido or "") + \
                    f"\nASSERT ERROR: operador desconocido {op_raw}"
                return False

        except Exception as e:
            ejec_paso.tipo_resultado = "error_tecnico"
            ejec_paso.valor_obtenido = (ejec_paso.valor_obtenido or "") + \
                f"\nASSERT ERROR: {str(e)}"
            return False

        if not ok:
            msg = getattr(a, "mensaje_error", None) or \
                  f"Assert falló: tipo={tipo}, expr={expr_text}, op={op_raw}, esperado={esperado}, valor={valor}"
            # Si venía ok/simulado/manual_ok, lo marcamos como fallo_assert
            if ejec_paso.tipo_resultado in (None, "ok", "simulado", "manual_ok"):
                ejec_paso.tipo_resultado = "fallo_assert"
            ejec_paso.valor_obtenido = (ejec_paso.valor_obtenido or "") + f"\n{msg}"
            return False

    return True


# ============================================================
# INICIALIZACIÓN DE EJECUCIÓN
# ============================================================

def _inicializar_ejecucion_pasos(db: Session, ejecucion: Ejecucion) -> None:
    """
    Crea EjecucionPaso en estado 'pendiente' para cada Paso del caso.
    No duplica si ya existen.
    """
    pasos_caso = (
        db.query(Paso)
        .options(
            joinedload(Paso.parametros).joinedload(ObjetoParametro.api)
        )
        .filter(Paso.caso_id == ejecucion.caso_id)
        .order_by(Paso.orden.asc())
        .all()
    )

    existentes = {ep.paso_id for ep in ejecucion.pasos}

    for paso in pasos_caso:
        if paso.id not in existentes:
            nuevo = EjecucionPaso(
                ejecucion_id=ejecucion.id,
                paso_id=paso.id,
                tipo_resultado="pendiente",
                request_json=None,
                response_json=None,
                asserts_json=None,
                errores_json=None,
                valor_obtenido="",
                duracion_ms=None,
                fecha=datetime.utcnow(),
                parametros_snapshot=None,
                asserts_snapshot=None,
            )
            db.add(nuevo)

    db.commit()
    db.refresh(ejecucion)


# ============================================================
# OBTENER SIGUIENTE PASO PENDIENTE
# ============================================================

def _get_siguiente_paso_pendiente(db: Session, ejecucion: Ejecucion):
    """
    Devuelve (EjecucionPaso, Paso) del siguiente paso pendiente.
    """
    ep = (
        db.query(EjecucionPaso)
        .join(Paso, Paso.id == EjecucionPaso.paso_id)
        .options(
            joinedload(EjecucionPaso.paso)
            .joinedload(Paso.parametros)
            .joinedload(ObjetoParametro.api)
        )
        .filter(
            EjecucionPaso.ejecucion_id == ejecucion.id,
            (EjecucionPaso.tipo_resultado == "pendiente") |
            (EjecucionPaso.tipo_resultado.is_(None)),
        )
        .order_by(Paso.orden.asc())
        .first()
    )

    if not ep:
        return None

    return ep, ep.paso


# ============================================================
# DETECTAR TIPO DE PASO
# ============================================================

def _detectar_tipo_paso(paso: Paso) -> str:
    """
    Devuelve:
    - 'automatico' si tiene API válida
    - 'simulado' si tiene API pero endpoint inválido
    - 'manual' si no tiene API
    """
    apis = {p.api for p in paso.parametros if p.api is not None}

    if len(apis) == 0:
        return "manual"

    if len(apis) > 1:
        raise HTTPException(
            status_code=400,
            detail="El paso tiene múltiples APIs asociadas. No está permitido.",
        )

    api = apis.pop()
    url = (api.endpoint or "").strip()

    if not url or not (url.startswith("http://") or url.startswith("https://")):
        return "simulado"

    return "automatico"


# ============================================================
# ACTUALIZAR ESTADO GLOBAL DE EJECUCIÓN
# ============================================================

def _actualizar_estado_ejecucion(db: Session, ejecucion: Ejecucion) -> None:
    """
    Actualiza estado, fecha_fin, resultado_global y porcentaje_aceptacion.
    """
    db.refresh(ejecucion)

    total = len(ejecucion.pasos)
    if total == 0:
        return

    pendientes = [
        ep for ep in ejecucion.pasos
        if ep.tipo_resultado in (None, "pendiente")
    ]

    ejecutados = [
        ep for ep in ejecucion.pasos
        if ep.tipo_resultado not in (None, "pendiente")
    ]

    if not pendientes and ejecutados:
        oks = sum(
            1
            for ep in ejecutados
            if ep.tipo_resultado in ("ok", "simulado", "manual_ok")
        )
        ejecucion.estado = "finalizado"
        ejecucion.fecha_fin = datetime.utcnow()
        ejecucion.resultado_global = "ok" if oks == len(ejecutados) else "error"
        ejecucion.porcentaje_aceptacion = round((oks / len(ejecutados)) * 100, 2)

    elif ejecutados and pendientes:
        ejecucion.estado = "en_progreso"

    db.commit()
    db.refresh(ejecucion)


# ============================================================
# SNAPSHOTS
# ============================================================

def _generar_snapshots_para_paso(
    paso: Paso
) -> tuple[list[dict[str, Any]] | None, list[dict[str, Any]] | None]:
    """
    Genera snapshots serializables de parámetros y asserts del paso.
    """
    if paso is None:
        return None, None

    parametros_snapshot = [
        {
            "nombre": p.nombre,
            "tipo": p.tipo,
            "valor_entrada": p.valor_entrada,
            "valor_esperado": p.valor_esperado,
        }
        for p in getattr(paso, "parametros", []) or []
    ]

    asserts_snapshot = [
        {
            "tipo": a.tipo,
            "expresion": a.expresion,
            "operador": a.operador,
            "valor_esperado": a.valor_esperado,
            "mensaje_error": a.mensaje_error,
            "orden": a.orden,
        }
        for a in getattr(paso, "asserts", []) or []
    ]

    return parametros_snapshot or None, asserts_snapshot or None
# ============================================================
# EJECUCIÓN AUTOMÁTICA REAL
# ============================================================

def _ejecutar_paso_automatico_real(
    db: Session,
    ejecucion: Ejecucion,
    ejec_paso: EjecucionPaso,
    paso: Paso,
    contexto: dict,
) -> None:
    """
    Ejecuta un paso real vía HTTP.
    Soporta body, header, query y path params.
    """
    contexto = contexto or {}

    # Snapshots del paso en el momento de la ejecución
    parametros_snapshot, asserts_snapshot = _generar_snapshots_para_paso(paso)
    ejec_paso.parametros_snapshot = parametros_snapshot
    ejec_paso.asserts_snapshot = asserts_snapshot

    apis = {p.api for p in paso.parametros if p.api is not None}
    api = apis.pop()

    url = reemplazar_variables(api.endpoint, contexto) or ""
    metodo = (api.metodo or "GET").upper()

    payload: dict = {}
    headers: dict = {}
    query: dict = {}

    for p in paso.parametros:
        entrada = reemplazar_variables(p.valor_entrada or "", contexto)

        if p.tipo == "body":
            payload[p.nombre] = entrada
        elif p.tipo == "header":
            headers[p.nombre] = entrada
        elif p.tipo == "query":
            query[p.nombre] = entrada
        elif p.tipo == "path":
            url = url.replace(f"{{{p.nombre}}}", str(entrada or ""))

    request_info = {
        "method": metodo,
        "url": url,
        "payload": payload,
        "headers": headers,
        "query": query,
    }

    inicio = datetime.utcnow()

    try:
        with httpx.Client(timeout=10) as client:
            response = client.request(
                method=metodo,
                url=url,
                json=payload or None,
                headers=headers or None,
                params=query or None,
            )

        try:
            data = response.json()
        except Exception:
            data = None

        response_info = {
            "status_code": response.status_code,
            "body": response.text,
            "json": data,
            "headers": dict(response.headers),
        }

        ejec_paso.request_json = request_info
        ejec_paso.response_json = response_info
        ejec_paso.valor_obtenido = json.dumps(
            {"request": request_info, "response": response_info},
            ensure_ascii=False,
        )

        estado_paso = "ok" if 200 <= response.status_code <= 299 else "error"

        # JSONPath → extracción y actualización de contexto
        for p in paso.parametros:
            if p.valor_esperado and p.valor_esperado.startswith("$."):
                try:
                    expr = parse(p.valor_esperado)
                    matches = [m.value for m in expr.find(data or {})]

                    if matches:
                        contexto[p.nombre] = str(matches[0])
                    else:
                        estado_paso = "error"
                except Exception:
                    estado_paso = "error"

        # Validación literal (solo el primero que no sea JSONPath)
        esperado_literal = next(
            (
                p.valor_esperado
                for p in paso.parametros
                if p.valor_esperado and not p.valor_esperado.startswith("$.")
            ),
            None,
        )

        if esperado_literal is not None:
            esperado_str = str(esperado_literal)
            contenido = (
                json.dumps(data, ensure_ascii=False) if data is not None else response.text
            )
            if esperado_str not in contenido:
                estado_paso = "error"

        # Estado base del paso
        ejec_paso.tipo_resultado = estado_paso

        # Evaluar asserts sobre la respuesta (puede marcar fallo_assert / error_tecnico)
        _evaluar_asserts(ejec_paso, paso, contexto)

    except Exception as e:
        ejec_paso.tipo_resultado = "error_tecnico"
        ejec_paso.valor_obtenido = f"ERROR: {str(e) or ''}"

    fin = datetime.utcnow()
    ejec_paso.duracion_ms = (fin - inicio).total_seconds() * 1000.0
    ejec_paso.fecha = fin

    db.commit()
    db.refresh(ejec_paso)


# ============================================================
# EJECUCIÓN AUTOMÁTICA SIMULADA
# ============================================================

def _ejecutar_paso_automatico_simulado(
    db: Session,
    ejecucion: Ejecucion,
    ejec_paso: EjecucionPaso,
    paso: Paso,
    contexto: dict,
) -> None:
    """
    Marca el paso como ejecutado en modo simulado.
    También ejecuta asserts si existen.
    """
    contexto = contexto or {}

    # Snapshots del paso en el momento de la ejecución
    parametros_snapshot, asserts_snapshot = _generar_snapshots_para_paso(paso)
    ejec_paso.parametros_snapshot = parametros_snapshot
    ejec_paso.asserts_snapshot = asserts_snapshot

    inicio = datetime.utcnow()

    ejec_paso.tipo_resultado = "simulado"
    ejec_paso.valor_obtenido = "Simulación exitosa"
    ejec_paso.fecha = inicio

    _evaluar_asserts(ejec_paso, paso, contexto)

    fin = datetime.utcnow()
    ejec_paso.duracion_ms = (fin - inicio).total_seconds() * 1000.0
    ejec_paso.fecha = fin

    db.commit()
    db.refresh(ejec_paso)


# ============================================================
# REGISTRO MANUAL
# ============================================================

def registrar_paso_manual(
    db: Session,
    ejecucion_id: int,
    paso_id: int,
    estado: str,
    resultado_texto: str,
) -> EjecucionPaso:
    ejecucion = _get_ejecucion_or_404(db, ejecucion_id)

    if ejecucion.estado == "finalizado":
        raise HTTPException(
            status_code=400,
            detail="No se puede registrar un paso manual en una ejecución finalizada",
        )

    ejec_paso = (
        db.query(EjecucionPaso)
        .filter(
            EjecucionPaso.ejecucion_id == ejecucion.id,
            EjecucionPaso.paso_id == paso_id,
        )
        .first()
    )

    if not ejec_paso:
        raise HTTPException(status_code=404, detail="Paso de ejecución no encontrado")

    if ejec_paso.tipo_resultado not in (None, "pendiente"):
        raise HTTPException(
            status_code=400,
            detail="No se puede ejecutar un paso ya ejecutado",
        )

    if estado not in ("ok", "error"):
        raise HTTPException(status_code=400, detail="Estado inválido")

    if not resultado_texto or not resultado_texto.strip():
        raise HTTPException(status_code=400, detail="Debe ingresar un resultado")

    # Snapshots del paso en el momento de la ejecución
    paso = ejec_paso.paso
    parametros_snapshot, asserts_snapshot = _generar_snapshots_para_paso(paso)
    ejec_paso.parametros_snapshot = parametros_snapshot
    ejec_paso.asserts_snapshot = asserts_snapshot

    ejec_paso.tipo_resultado = "manual_ok" if estado == "ok" else "manual_error"
    ejec_paso.valor_obtenido = str(resultado_texto.strip() or "")
    ejec_paso.fecha = datetime.utcnow()

    db.commit()
    db.refresh(ejec_paso)

    _actualizar_estado_ejecucion(db, ejecucion)

    return ejec_paso


# ============================================================
# EJECUTAR SIGUIENTE PASO
# ============================================================

def ejecutar_siguiente_paso(db: Session, ejecucion_id: int) -> Ejecucion:
    ejecucion = _get_ejecucion_or_404(db, ejecucion_id)

    if ejecucion.estado == "finalizado":
        raise HTTPException(status_code=400, detail="La ejecución ya está finalizada")

    _inicializar_ejecucion_pasos(db, ejecucion)

    siguiente = _get_siguiente_paso_pendiente(db, ejecucion)
    if not siguiente:
        _actualizar_estado_ejecucion(db, ejecucion)
        return ejecucion

    # Aseguramos contexto dict persistente
    if ejecucion.contexto is None:
        ejecucion.contexto = {}
        db.commit()
        db.refresh(ejecucion)

    contexto = ejecucion.contexto or {}

    ejec_paso, paso = siguiente
    tipo = _detectar_tipo_paso(paso)

    if tipo == "manual":
        raise HTTPException(status_code=400, detail="El siguiente paso es manual")

    if tipo == "automatico":
        _ejecutar_paso_automatico_real(db, ejecucion, ejec_paso, paso, contexto)
    else:
        _ejecutar_paso_automatico_simulado(db, ejecucion, ejec_paso, paso, contexto)

    # Persistimos contexto actualizado
    ejecucion.contexto = contexto
    db.commit()
    db.refresh(ejecucion)

    _actualizar_estado_ejecucion(db, ejecucion)
    return ejecucion


# ============================================================
# EJECUTAR EJECUCIÓN COMPLETA
# ============================================================

def ejecutar_ejecucion(db: Session, ejecucion_id: int) -> Ejecucion:
    ejecucion = _get_ejecucion_or_404(db, ejecucion_id)

    if ejecucion.estado == "finalizado":
        raise HTTPException(status_code=400, detail="La ejecución ya está finalizada")

    _inicializar_ejecucion_pasos(db, ejecucion)

    if ejecucion.estado == "pendiente":
        ejecucion.estado = "en_progreso"
        db.commit()
        db.refresh(ejecucion)

    # Aseguramos contexto dict persistente
    if ejecucion.contexto is None:
        ejecucion.contexto = {}
        db.commit()
        db.refresh(ejecucion)

    modo = (ejecucion.modo or "mixto").lower()
    contexto = ejecucion.contexto or {}

    if modo == "paso_a_paso":
        return ejecutar_siguiente_paso(db, ejecucion_id)

    while True:
        siguiente = _get_siguiente_paso_pendiente(db, ejecucion)
        if not siguiente:
            break

        ejec_paso, paso = siguiente
        tipo = _detectar_tipo_paso(paso)

        if tipo == "manual":
            if modo in ("automatico", "mixto"):
                break

        if tipo == "automatico":
            _ejecutar_paso_automatico_real(db, ejecucion, ejec_paso, paso, contexto)
        else:
            _ejecutar_paso_automatico_simulado(db, ejecucion, ejec_paso, paso, contexto)

        # Persistimos contexto actualizado después de cada paso
        ejecucion.contexto = contexto
        db.commit()
        db.refresh(ejecucion)

    _actualizar_estado_ejecucion(db, ejecucion)
    return ejecucion
