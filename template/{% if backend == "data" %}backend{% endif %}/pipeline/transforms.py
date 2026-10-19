"""Pure transformations: a DataFrame in, a DataFrame out, no side effect."""

import polars as pl


def monthly_totals(measurements: pl.DataFrame) -> pl.DataFrame:
    """Total of the values per month and category, sorted by month then category."""
    return (
        measurements.with_columns(pl.col("date").dt.truncate("1mo").alias("month"))
        .group_by("month", "category")
        .agg(pl.col("value").sum().alias("total"))
        .sort("month", "category")
    )
