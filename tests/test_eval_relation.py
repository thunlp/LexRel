import json
from pathlib import Path
import runpy
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "Code" / "eval" / "eval_relation.py"
INPUT_PATH = "/path/to/data/fixture_type.json"


def expected_metrics(rows):
    # Include the row number so relations only match within the same example.
    predicted = {(row, label) for row, (labels, _) in enumerate(rows) for label in labels}
    gold = {(row, label) for row, (_, labels) in enumerate(rows) for label in labels}
    matches = len(predicted & gold)
    precision = matches / len(predicted) if predicted else 0.0
    recall = matches / len(gold) if gold else 0.0
    f1 = 2 * matches / (len(predicted) + len(gold)) if predicted or gold else 0.0
    return precision, recall, f1


@pytest.mark.parametrize(
    "rows",
    [
        [(["借贷", "担保"], ["借贷", "担保"])],
        [(["借贷"], ["借贷", "担保"])],
        [(["借贷", "担保", "租赁"], ["借贷", "担保"])],
        [(["借贷", "租赁"], ["借贷", "担保"])],
        [([], ["借贷"])],
        [(["借贷"], [])],
        [([], [])],
        [(["借贷", "担保", "租赁"], ["借贷", "担保"]),
         (["保管"], ["租赁", "保管", "运输"])],
    ],
    ids=["perfect", "no-false-positives", "no-false-negatives", "mixed",
         "no-predictions", "no-gold", "both-empty", "multi-row-micro"],
)
def test_relation_cli_reports_micro_metrics(rows, tmp_path, monkeypatch, capsys):
    fixture = tmp_path / "fixture_type.json"
    fixture.write_text(
        json.dumps([
            {"predict_relation": predicted, "relation": dict.fromkeys(gold, [])}
            for predicted, gold in rows
        ], ensure_ascii=False),
        encoding="utf-8",
    )

    original_open = open

    def open_fixture(path, *args, **kwargs):
        return original_open(fixture if path == INPUT_PATH else path, *args, **kwargs)

    # Run the script entry point using its own argparse, JSON parsing and formatting.
    with monkeypatch.context() as script:
        script.setattr("builtins.open", open_fixture)
        script.setattr(sys, "argv", [str(SCRIPT), "--model", "fixture"])
        runpy.run_path(str(SCRIPT), run_name="__main__")

    precision, recall, f1 = expected_metrics(rows)
    assert capsys.readouterr().out == (
        f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}\n"
    )
