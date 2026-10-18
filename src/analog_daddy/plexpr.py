"""A collection of polars expressions/idioms which I find useful.

These expressions might change over time, based on how my understanding improves,
as well as based on feedback. Use them as a template.
These should probably be a docs page, but I also value their reusability
without having to resort to copy-pasting snippets everytime I need them.
"""

import polars as pl


def minmax_at_x(x: pl.Expr, y: pl.Expr) -> tuple[pl.Expr, ...]:
    """
    Get a polars expression to compute min, max of a column along with values at which it occurs.

    This function can give different answers if there is a tie at min or max value.

    Parameters
    ----------
    x : pl.Expr
        The column to compute min and max across.
    y : pl.Expr
        The column to compute min and max for.

    References
    ----------
    - I unfortunately found this [resource](https://code-examples.net/en/q/4bb4f9a/how-to-use-min-by-in-polars-to-solve-correlated-min-max) a bit later and it would have saved me some frustration in validating if my approach was the idiomatic.

    Examples
    --------
    >>> (df := pl.DataFrame({"x": ["A", "B", "C", "D"], "y": [1, 2, 3, 4]}))
    shape: (4, 2)
    ┌─────┬─────┐
    │ x   ┆ y   │
    │ --- ┆ --- │
    │ str ┆ i64 │
    ╞═════╪═════╡
    │ A   ┆ 1   │
    │ B   ┆ 2   │
    │ C   ┆ 3   │
    │ D   ┆ 4   │
    └─────┴─────┘
    >>> df.select(minmax_at_x(pl.col("x"), pl.col("y")))
    shape: (1, 4)
    ┌────────┬─────────────┬────────┬─────────────┐
    │ min__y ┆ x_at_min__y ┆ max__y ┆ x_at_max__y │
    │ ---    ┆ ---         ┆ ---    ┆ ---         │
    │ i64    ┆ str         ┆ i64    ┆ str         │
    ╞════════╪═════════════╪════════╪═════════════╡
    │ 1      ┆ A           ┆ 4      ┆ D           │
    └────────┴─────────────┴────────┴─────────────┘
    """
    if y.meta.has_multiple_outputs():
        raise ValueError(f"{y} must be a single column")
    if x.meta.has_multiple_outputs():
        raise ValueError(f"{x} must be a single column")

    yn = y.meta.output_name()
    xn = x.meta.output_name()

    return (
        y.min().name.prefix("min__"),
        x.min_by(y).alias(f"{xn}_at_min__{yn}"),
        y.max().name.prefix("max__"),
        x.max_by(y).alias(f"{xn}_at_max__{yn}"),
    )


def minmax_at_x_alt(x: pl.Expr, y: pl.Expr) -> tuple[pl.Expr, ...]:
    """
    Alternate implementation of a ``minmax_at_x``.

    This function can give different answers if there is a tie at min or max value.

    Parameters
    ----------
    x : pl.Expr
        The column to compute min and max across.
    y : pl.Expr
        The column to compute min and max for.

    References
    ----------
    - I unfortunately found this [resource](https://code-examples.net/en/q/4bb4f9a/how-to-use-min-by-in-polars-to-solve-correlated-min-max) a bit later and it would have saved me some frustration in validating if my approach was the idiomatic.

    Examples
    --------
    >>> (df := pl.DataFrame({"x": ["A", "B", "C", "D"], "y": [1, 2, 3, 4]}))
    shape: (4, 2)
    ┌─────┬─────┐
    │ x   ┆ y   │
    │ --- ┆ --- │
    │ str ┆ i64 │
    ╞═════╪═════╡
    │ A   ┆ 1   │
    │ B   ┆ 2   │
    │ C   ┆ 3   │
    │ D   ┆ 4   │
    └─────┴─────┘
    >>> df.select(minmax_at_x_alt(pl.col("x"), pl.col("y")))
    shape: (1, 4)
    ┌────────┬─────────────┬────────┬─────────────┐
    │ min__y ┆ x_at_min__y ┆ max__y ┆ x_at_max__y │
    │ ---    ┆ ---         ┆ ---    ┆ ---         │
    │ i64    ┆ str         ┆ i64    ┆ str         │
    ╞════════╪═════════════╪════════╪═════════════╡
    │ 1      ┆ A           ┆ 4      ┆ D           │
    └────────┴─────────────┴────────┴─────────────┘
    """
    if y.meta.has_multiple_outputs():
        raise ValueError(f"{y} must be a single column")
    if x.meta.has_multiple_outputs():
        raise ValueError(f"{x} must be a single column")

    yn = y.meta.output_name()
    xn = x.meta.output_name()

    return (
        y.min().name.prefix("min__"),
        x.get(y.arg_min()).alias(f"{xn}_at_min__{yn}"),
        y.max().name.prefix("max__"),
        x.get(y.arg_max()).alias(f"{xn}_at_max__{yn}"),
    )


def minmax_mean_ksigma(y: pl.Expr, k: float = 1.0) -> tuple[pl.Expr, ...]:
    """Get a polars expression to compute min, max and statistics of a column.

    Examples
    --------
    >>> import numpy as np
    >>> mean, std_dev = 10, 2
    >>> a = pl.DataFrame(
    ...     {
    ...         "x": np.random.default_rng(seed=12345).normal(loc=mean, scale=std_dev, size=1200),
    ...     }
    ... ).with_row_index(offset=1)
    >>> a.select(minmax_mean_ksigma(pl.col("x"))).select(pl.all().cast(pl.Decimal(scale=2))).unpivot()
    shape: (6, 2)
    ┌─────────────────┬───────────────┐
    │ variable        ┆ value         │
    │ ---             ┆ ---           │
    │ str             ┆ decimal[38,2] │
    ╞═════════════════╪═══════════════╡
    │ min__x          ┆ 3.76          │
    │ mean - 1*std__x ┆ 8.05          │
    │ mean__x         ┆ 10.07         │
    │ mean + 1*std__x ┆ 12.09         │
    │ max__x          ┆ 16.92         │
    │ std__x          ┆ 2.02          │
    └─────────────────┴───────────────┘
    """
    if y.meta.has_multiple_outputs():
        raise ValueError(f"{y} must be a single column")

    yn = y.meta.output_name()
    mean = y.mean()
    sigma = y.std()

    return (
        y.min().name.prefix("min__"),
        (mean - k * sigma).alias(f"mean - {k:g}*std__{yn}"),
        mean.name.prefix("mean__"),
        (mean + k * sigma).alias(f"mean + {k:g}*std__{yn}"),
        y.max().name.prefix("max__"),
        sigma.name.prefix("std__"),
    )
