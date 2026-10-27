import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def test_retrieval_golden_points_to_existing_runbooks():
    runbooks = {p.stem for p in (DATA / "runbooks").glob("*.md") if p.stem != "README"}
    rows = [json.loads(line) for line in (DATA / "retrieval_golden.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]

    assert len(rows) >= 12
    assert {r["expected_runbook"] for r in rows} <= runbooks
    assert len({r["id"] for r in rows}) == len(rows)
