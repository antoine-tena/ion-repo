"""Committed trained models, tied to the code that made them ([MODEL-TRACED]).

Next to each model of `data/models/`, a manifest `<model>.manifest.json` written by the training
command: the hash of the training code, the seed, the version of the dataset and the metrics.
`tests/test_models.py` fails when the code changed since (the model is stale: retrain it, or say
why in the commit) and when the model now scores below its recorded metrics.
"""

import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent / "data" / "models"
MANIFEST_SUFFIX = ".manifest.json"
# How much a metric may move between two runs of the same code (floating point, threads).
METRIC_TOLERANCE = 1e-6


@dataclass(frozen=True)
class Manifest:
    model: Path
    code: tuple[str, ...]  # training code, relative to the backend folder
    code_sha256: str
    seed: int
    dataset: str
    metrics: Mapping[str, float]


def code_hash(code: Sequence[str], root: Path = MODELS_DIR.parent.parent) -> str:
    """SHA-256 of the training code, file by file in a stable order."""
    digest = hashlib.sha256()
    for name in sorted(code):
        digest.update(name.encode())
        digest.update((root / name).read_bytes())
    return digest.hexdigest()


def write_manifest(
    model: Path,
    *,
    code: Sequence[str],
    seed: int,
    dataset: str,
    metrics: Mapping[str, float],
    root: Path = MODELS_DIR.parent.parent,
) -> Path:
    """Called by the training command, right after it saved `model`."""
    manifest = model.with_name(model.name + MANIFEST_SUFFIX)
    record = {
        "code": sorted(code),
        "code_sha256": code_hash(code, root),
        "seed": seed,
        "dataset": dataset,
        "metrics": dict(metrics),
    }
    manifest.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def manifests(directory: Path = MODELS_DIR) -> list[Manifest]:
    found = []
    for path in sorted(directory.glob(f"*{MANIFEST_SUFFIX}")) if directory.is_dir() else ():
        record = json.loads(path.read_text(encoding="utf-8"))
        found.append(
            Manifest(
                model=path.with_name(path.name.removesuffix(MANIFEST_SUFFIX)),
                code=tuple(record["code"]),
                code_sha256=record["code_sha256"],
                seed=int(record["seed"]),
                dataset=str(record["dataset"]),
                metrics={name: float(value) for name, value in record["metrics"].items()},
            )
        )
    return found


# The project's evaluation of a committed model on the committed sample, by model file name:
# `EVALUATORS["classifier.joblib"] = evaluate_classifier`, returning the manifest's metrics.
EVALUATORS: dict[str, Callable[[Path], Mapping[str, float]]] = {}
