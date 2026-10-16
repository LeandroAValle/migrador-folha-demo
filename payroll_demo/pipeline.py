"""Deterministic, offline migration simulator. No production adapters or credentials."""

from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

SEED = 202610
PERIOD = "2026-09"
ENTITIES = ("Servidor", "Vínculo", "Rubrica", "Lançamento")
PHASES = ("Extrair", "Validar", "Transformar", "Enviar lote simulado", "Conciliar")


def source_rows() -> list[dict]:
    """Generate a small, explicitly fictional legacy dataset."""
    rng = random.Random(SEED)
    rows = []
    for entity, count in zip(ENTITIES, (48, 52, 18, 120), strict=True):
        for index in range(1, count + 1):
            amount = round(rng.uniform(900, 5600), 2) if entity == "Lançamento" else None
            rows.append({
                "sourceKey": f"{entity[:3].upper()}-{index:04d}",
                "entity": entity,
                "period": PERIOD,
                "unit": ("Unidade Aurora", "Unidade Horizonte", "Unidade Vale")[index % 3],
                "amount": amount,
                "requiredCode": "" if index % 29 == 0 else f"COD-{index:03d}",
            })
    return rows


def validate_row(row: dict) -> str | None:
    if not row["requiredCode"]:
        return "Código obrigatório ausente na origem fictícia"
    if row["entity"] == "Lançamento" and (row["amount"] is None or row["amount"] <= 0):
        return "Valor do lançamento inválido"
    return None


def transform_row(row: dict) -> dict:
    """Generic illustrative payload, intentionally unrelated to any provider schema."""
    return {
        "externalKey": row["sourceKey"],
        "category": row["entity"],
        "referencePeriod": row["period"],
        "organizationalUnit": row["unit"],
        "amount": row["amount"],
        "code": row["requiredCode"],
    }


def simulate_provider(payload: dict) -> tuple[str, str]:
    """Fixed fake responses that exercise success and error handling."""
    serial = int(payload["externalKey"].split("-")[-1])
    if serial % 23 == 0:
        return "ERRO", "Destino simulado rejeitou o registro para revisão"
    return "EXECUTADO", "Aceito pelo destino simulado"


def build_snapshot() -> dict:
    source = source_rows()
    keys = [row["sourceKey"] for row in source]
    if len(keys) != len(set(keys)):
        raise ValueError("Chaves de origem duplicadas")

    control = []
    for row in source:
        reason = validate_row(row)
        history = ["EXTRAIDO", "VALIDADO"]
        payload = None
        if reason:
            status = "ERRO"
            history.append(status)
        else:
            payload = transform_row(row)
            history.extend(("PENDENTE", "ENVIADO"))
            status, reason = simulate_provider(payload)
            history.append(status)
        control.append({
            "sourceKey": row["sourceKey"],
            "entity": row["entity"],
            "unit": row["unit"],
            "status": status,
            "history": history,
            "message": reason,
            "payload": payload,
        })

    counts = Counter(item["status"] for item in control)
    by_entity = []
    for entity in ENTITIES:
        records = [item for item in control if item["entity"] == entity]
        by_entity.append({
            "entity": entity,
            "extracted": len(records),
            "completed": sum(item["status"] == "EXECUTADO" for item in records),
            "errors": sum(item["status"] == "ERRO" for item in records),
        })

    snapshot = {
        "schemaVersion": 1,
        "period": PERIOD,
        "source": "synthetic",
        "destination": "offline simulator",
        "batchSize": 25,
        "phases": PHASES,
        "metrics": {
            "extracted": len(source),
            "completed": counts["EXECUTADO"],
            "errors": counts["ERRO"],
            "validated": sum("PENDENTE" in item["history"] for item in control),
            "batches": (sum("PENDENTE" in item["history"] for item in control) + 24) // 25,
        },
        "byEntity": by_entity,
        "control": control,
    }
    assert snapshot["metrics"]["extracted"] == snapshot["metrics"]["completed"] + snapshot["metrics"]["errors"]
    assert all(item["sourceKey"] == item["payload"]["externalKey"] for item in control if item["payload"])
    return snapshot


def export_snapshot(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_snapshot(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
