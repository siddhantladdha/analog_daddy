"""Utilities for working with Polars DataFrames."""

import re

import polars as pl
from quantiphy import InvalidNumber, as_real

_COL_RE = re.compile(
    r"""
            col # literal
            \( # literal (
            "  # literal "
            (?P<var>\w+) # variable name
            "  # literal "
            \) # literal )
        """,
    re.VERBOSE,
)


def drop_all_null(df: pl.DataFrame) -> pl.DataFrame:
    """Drop columns where every value is null.

    Parameters
    ----------
    df : pl.DataFrame
        DataFrame to clean up.

    Returns
    -------
    pl.DataFrame
        DataFrame with all-null columns removed.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [None, None, None],
    ...         "b": [1, 2, None],
    ...         "c": ["x", "y", ""],
    ...     }
    ... )
    >>> drop_all_null(df).columns
    ['b', 'c']
    """
    return df[[ser.name for ser in df if ser.null_count() != df.height]]


def filter_all_null(df: pl.DataFrame) -> pl.DataFrame:
    """Filter out rows from a dataframe where every value is null.

    Parameters
    ----------
    df : pl.DataFrame
        DataFrame to filter.

    Returns
    -------
    pl.DataFrame
        DataFrame with all-null rows removed.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, None, 3],
    ...         "b": ["x", None, None],
    ...     }
    ... )
    >>> filter_all_null(df)
    shape: (2, 2)
    ┌─────┬──────┐
    │ a   ┆ b    │
    │ --- ┆ ---  │
    │ i64 ┆ str  │
    ╞═════╪══════╡
    │ 1   ┆ x    │
    │ 3   ┆ null │
    └─────┴──────┘
    """
    return df.filter(~pl.all_horizontal(pl.all().is_null()))


def _extract_first_parameter_keys(
    df: pl.DataFrame,
    scan_col: str,
    identify_str: str = "Parameters:",
    key_split: str = "=",
    pair_split: str = ",",
) -> list[str]:
    """Read a DataFrame for the first matching row of identify_str. Extract the key names from the row using the key_split and pair_split.

    Parameters
    ----------
    df : pl.DataFrame
        DataFrame to scan for the row.
    scan_col : str
        Column to scan for the identifying row.
    identify_str : str, default "Parameters:"
        String that identifies the row to extract keys from.
    key_split : str, default "="
        String that separates keys from values in the row.
    pair_split : str, default ","
        String that separates key-value pairs in the row.

    Returns
    -------
    list[str]
        Ordered list of parameter names found in the first matching row.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "Point": [
    ...             "Parameters: var1=-12k, var_b=1n",
    ...             "1",
    ...             "Parameters: var3=-12k",
    ...             "2",
    ...         ],
    ...         "Value": [None, 10, 1, None],
    ...     }
    ... )
    >>> _extract_first_parameter_keys(df, scan_col="Point")
    ['var1', 'var_b']
    """
    first: str | None = df.select(
        pl.col(scan_col).filter(pl.col(scan_col).str.starts_with(identify_str)).first(ignore_nulls=True)
    ).item()

    if not first:
        raise ValueError(f"No row found starting with {identify_str}")
    first = first.replace(" ", "").removeprefix(identify_str)
    return [pair.split(re.escape(key_split))[0] for pair in first.split(re.escape(pair_split))]


def explode_nested_params(
    df: pl.DataFrame,
    keys: list[str],
    index_col: str = "Point",
    identify_str: str = "Parameters:",
) -> pl.DataFrame:
    """Turn inline ``key=value`` parameter rows into columns on the data rows below them.

    Parameters
    ----------
    df : pl.DataFrame
        DataFrame with interleaved parameter/data rows.
    keys : list[str]
        Ordered parameter key names, e.g. from `extract_param_keys`.
    index_col : str, default "Point"
        Column that carries the parameter marker rows.
    identify_str : str, default "Parameters:"
        Prefix string that identifies a parameter row.

    Returns
    -------
    pl.DataFrame
        Data rows only, with one new column per key in `keys`.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "Point": ["Parameters: ds=0, gs=1", "1", "2"],
    ...         "Value": [None, 10, 20],
    ...     }
    ... )
    >>> explode_nested_params(df, keys=["ds", "gs"])
    shape: (2, 4)
    ┌───────┬───────┬─────┬─────┐
    │ Point ┆ Value ┆ ds  ┆ gs  │
    │ ---   ┆ ---   ┆ --- ┆ --- │
    │ str   ┆ i64   ┆ str ┆ str │
    ╞═══════╪═══════╪═════╪═════╡
    │ 1     ┆ 10    ┆ 0   ┆ 1   │
    │ 2     ┆ 20    ┆ 0   ┆ 1   │
    └───────┴───────┴─────┴─────┘
    """
    is_param_row = pl.col(index_col).str.starts_with(identify_str)
    param_re = ", ".join(rf"{k}=(?P<{k}>[^,]+)" for k in keys)
    return (
        df.with_columns(pl.when(is_param_row).then(pl.col(index_col)).otherwise(None).forward_fill().alias("param_str"))
        .filter(~is_param_row)
        .with_columns(pl.col("param_str").str.extract_groups(param_re).alias("params"))
        .unnest("params")
        .drop("param_str")
    )


def _parse_operand(operand: str, pattern: re.Pattern[str] = _COL_RE) -> pl.Expr:
    """Parse an operand with SI prefixes and/or column references to a polars expression.

    Examples
    --------
    >>> _parse_operand("10m").meta.eq(pl.lit(0.01))
    True
    >>> _parse_operand('col("foo")').meta.eq(pl.col("foo"))
    True
    """
    if match := pattern.fullmatch(f"{operand}"):
        return pl.col(match.group("var"))
    return pl.lit(as_real(operand))


def spec(
    col: pl.Expr,
    spec: str,
    _near_tolerance: float = 0,
) -> pl.Expr:
    r"""
    Parse a specification string into a boolean pass/fail ``pl.Expr`` over ``col``.

    The spec string allows an ergonomic grammer for specifying constraints.
    - Supports SI-prefixes using quantiphy (e.g. ``10m`` = 0.01, ``0.01k`` = 10)
    - Supports simple column references ``col("name")``, which resolves to ``pl.col("name")``.

    TODO: Support ternary of pass/fail and near using _near_tolerance in future.

    Parameters
    ----------
    col : pl.Expr
        The column expression to test against the spec.
    spec : str
        The spec string to parse.

    Returns
    -------
    pl.Expr
        A boolean expression that evaluates to True if the value in ``col``
        satisfies the spec, and False otherwise.

    Examples
    --------
    >>> df = pl.from_repr(r'''shape: (2, 3)
    ... ┌──────┬──────┬─────┐
    ... │ x    ┆ foo  ┆ bar │
    ... │ ---  ┆ ---  ┆ --- │
    ... │ f64  ┆ f64  ┆ f64 │
    ... ╞══════╪══════╪═════╡
    ... │ 9.0  ┆ 10.0 ┆ 5.0 │
    ... │ 11.0 ┆ 10.0 ┆ 5.0 │
    ... └──────┴──────┴─────┘
    ... ''')
    >>> lit_specs = [
    ...     "> 10m",
    ...     "< 0.01k",
    ...     "range 8000m 10500m",
    ...     "tolerance 10 20",
    ... ]
    >>> df.select(*(spec(pl.col("x"), s).alias(s) for s in lit_specs))
    shape: (2, 4)
    ┌───────┬─────────┬────────────────────┬─────────────────┐
    │ > 10m ┆ < 0.01k ┆ range 8000m 10500m ┆ tolerance 10 20 │
    │ ---   ┆ ---     ┆ ---                ┆ ---             │
    │ bool  ┆ bool    ┆ bool               ┆ bool            │
    ╞═══════╪═════════╪════════════════════╪═════════════════╡
    │ true  ┆ true    ┆ true               ┆ true            │
    │ true  ┆ false   ┆ false              ┆ true            │
    └───────┴─────────┴────────────────────┴─────────────────┘
    >>> calc_specs = {
    ...     "range": 'range col("bar") col("foo")',
    ...     "gt": '> col("foo")',
    ...     "tol": 'tolerance col("foo") col("bar")',
    ... }
    >>> print(df.select(*(spec(pl.col("x"), s).alias(name) for name, s in calc_specs.items())).write_csv())
    range,gt,tol
    true,false,false
    false,true,false
    <BLANKLINE>
    """
    operator, *vals = spec.split()
    try:
        vals = [_parse_operand(v) for v in vals]
    except InvalidNumber:
        raise ValueError(f"bad numbers {vals} in spec: {spec}")

    match operator:
        case ">":
            return col.gt(vals[0])
        case "<":
            return col.lt(vals[0])
        case "range":
            lo, hi = vals
            return col.is_between(lo, hi)
        case "tolerance" | "tol":  # "tolerance 10 2" -> 10 +/- 2%"
            val, tol_pct = vals
            tol_abs = abs(val) * tol_pct / 100
            return col.is_between(val - tol_abs, val + tol_abs)
    raise ValueError(f"bad spec: {spec}")


def cleanup(df: pl.DataFrame, delimiter: str) -> pl.DataFrame:
    """Basic clean-up of DataFrame."""
    return (
        # firstly we remove empty rows.
        df.pipe(filter_all_null)
        # then fill the DELIM_COL with junk to keep it.
        .with_columns(pl.lit("|").alias(delimiter))
        # finally drop any empty columns.
        .pipe(drop_all_null)
    )
