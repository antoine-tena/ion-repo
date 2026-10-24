"""The committed models still match their code and their metrics ([MODEL-TRACED])."""

import pytest

from pipeline.models import EVALUATORS, METRIC_TOLERANCE, Manifest, code_hash, manifests

MANIFESTS = manifests()


@pytest.mark.parametrize("manifest", MANIFESTS, ids=[m.model.name for m in MANIFESTS])
def test_a_committed_model_was_trained_by_the_current_code(manifest: Manifest) -> None:
    assert manifest.model.is_file(), f"{manifest.model.name}: manifest without its model"
    assert code_hash(manifest.code) == manifest.code_sha256, (
        f"{manifest.model.name}: its training code changed since: retrain it, "
        "or rewrite its manifest and say why in the commit"
    )


@pytest.mark.parametrize("manifest", MANIFESTS, ids=[m.model.name for m in MANIFESTS])
def test_a_committed_model_keeps_its_recorded_metrics(manifest: Manifest) -> None:
    evaluate = EVALUATORS.get(manifest.model.name)
    if evaluate is None:
        pytest.skip(f"{manifest.model.name}: no evaluator in pipeline.models.EVALUATORS")
    measured = evaluate(manifest.model)
    for name, recorded in manifest.metrics.items():
        assert measured[name] >= recorded - METRIC_TOLERANCE, (
            f"{name}: {measured[name]} < {recorded}"
        )
