"""Loading of the datasets, validated at the edge ([VALIDATE-AT-BOUNDARIES])."""

from pathlib import Path

import polars as pl

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SAMPLE_MEASUREMENTS = DATA_DIR / "sample" / "measurements.csv"

MEASUREMENTS_SCHEMA = pl.Schema({"date": pl.Date, "category": pl.String, "value": pl.Float64})


class DatasetSchemaError(ValueError):
    """Unexpected columns or types: loading fails, not the figure."""


def load_measurements(path: Path = SAMPLE_MEASUREMENTS) -> pl.DataFrame:
    """Dated measurements by category; columns and types checked before any use."""
    measurements = pl.read_csv(path, try_parse_dates=True)
    missing_columns = set(MEASUREMENTS_SCHEMA.names()) - set(measurements.columns)
    if missing_columns:
        raise DatasetSchemaError(f"missing columns in {path.name}: {sorted(missing_columns)}")
    try:
        return measurements.select(MEASUREMENTS_SCHEMA.names()).cast(MEASUREMENTS_SCHEMA)
    except pl.exceptions.InvalidOperationError as error:
        raise DatasetSchemaError(f"unexpected types in {path.name}") from error
