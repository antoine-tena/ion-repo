import json
from pathlib import Path

from pipeline.models import code_hash, manifests, write_manifest


def test_a_manifest_records_the_code_that_trained_the_model(tmp_path: Path) -> None:
    (tmp_path / "train.py").write_text("SEED = 7\n")
    model = tmp_path / "model.bin"
    model.write_bytes(b"weights")

    manifest = write_manifest(
        model,
        code=["train.py"],
        seed=7,
        dataset="sample-v1",
        metrics={"accuracy": 0.9},
        root=tmp_path,
    )

    record = json.loads(manifest.read_text())
    assert record["code_sha256"] == code_hash(["train.py"], tmp_path)
    assert manifests(tmp_path)[0].metrics == {"accuracy": 0.9}
    (tmp_path / "train.py").write_text("SEED = 8\n")
    assert code_hash(["train.py"], tmp_path) != record["code_sha256"]
