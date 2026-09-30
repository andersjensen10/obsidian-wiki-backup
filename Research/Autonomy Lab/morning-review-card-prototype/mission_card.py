#!/usr/bin/env python3
"""Deterministic, fixture-only Morning Review Card renderer.

This prototype deliberately reads supplied JSON only. It never contacts LAN
services, Townhall, Hermes, or the Kitchen Wall.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TEXT = (
    "missionId",
    "selectedAt",
    "hypothesis",
    "deferOrPreemptRule",
    "sandboxBoundary",
    "promotionDecision",
    "morningQuestion",
    "rollback",
)
REQUIRED_LISTS = ("candidateSources", "measurableSignals", "evidencePaths")
RESOURCE_CLASSES = {"none", "local-cpu", "spark"}
ADMISSION_STATES = {"not-required", "idle", "busy", "unreadable"}


class MissionCardError(ValueError):
    pass


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def validate(card: dict[str, Any]) -> None:
    if not isinstance(card, dict):
        raise MissionCardError("card must be a JSON object")
    for field in REQUIRED_TEXT:
        if not _nonempty_text(card.get(field)):
            raise MissionCardError(f"{field} must be a non-empty string")
    for field in REQUIRED_LISTS:
        values = card.get(field)
        if not isinstance(values, list) or not values or not all(_nonempty_text(v) for v in values):
            raise MissionCardError(f"{field} must be a non-empty list of strings")

    resource_class = card.get("resourceClass")
    if resource_class not in RESOURCE_CLASSES:
        raise MissionCardError("resourceClass must be one of: none, local-cpu, spark")

    admission = card.get("admissionSnapshot")
    if not isinstance(admission, dict):
        raise MissionCardError("admissionSnapshot must be an object")
    state = admission.get("state")
    if state not in ADMISSION_STATES:
        raise MissionCardError("admissionSnapshot.state must be not-required, idle, busy, or unreadable")

    if resource_class == "spark" and state == "not-required":
        raise MissionCardError("Spark missions require an admission snapshot")
    if resource_class != "spark" and state != "not-required":
        raise MissionCardError("non-Spark missions must use admissionSnapshot.state = not-required")
    if resource_class == "spark" and state in {"busy", "unreadable"} and card["promotionDecision"] != "deferred":
        raise MissionCardError("busy or unreadable Spark admission requires promotionDecision = deferred")


def render(card: dict[str, Any]) -> str:
    validate(card)
    admission = card["admissionSnapshot"]
    status = "DEFERRED" if card["resourceClass"] == "spark" and admission["state"] in {"busy", "unreadable"} else "READY FOR REVIEW"
    details = admission.get("details", "No additional details recorded.")
    return f"""---
type: morning-review-card
missionId: {card['missionId']}
selectedAt: {card['selectedAt']}
status: {status.lower().replace(' ', '-')}
resourceClass: {card['resourceClass']}
---

# Morning Review Card — {card['missionId']}

**Status:** {status}  
**Selected:** {card['selectedAt']}  
**Resource class:** {card['resourceClass']}

## Hypothesis
{card['hypothesis']}

## Why this was selected
{_bullets(card['candidateSources'])}

## Resource admission
- **State:** {admission['state']}
- **Evidence:** {details}
- **Yield rule:** {card['deferOrPreemptRule']}

## Sandbox and rollback
- **Boundary:** {card['sandboxBoundary']}
- **Rollback:** {card['rollback']}

## Measurable signals
{_bullets(card['measurableSignals'])}

## Evidence paths
{_bullets(card['evidencePaths'])}

## Promotion decision
{card['promotionDecision']}

## Morning question
**{card['morningQuestion']}**
"""


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: mission_card.py INPUT.json OUTPUT.md", file=sys.stderr)
        return 2
    source, output = map(Path, argv[1:])
    try:
        card = json.loads(source.read_text(encoding="utf-8"))
        rendered = render(card)
    except (OSError, json.JSONDecodeError, MissionCardError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
