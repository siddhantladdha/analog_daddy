"""A module to define semantic roles of columns in a DataFrame.

Examples
--------
>>> import polars as pl
>>> import polars.selectors as cs
>>> df = pl.DataFrame(
...     {
...         "x1": [1, 2, 3],
...         "x2": ["a", "b", "c"],
...         "delimiter": [0, 0, 0],
...         "y1": [4, 5, 6],
...         "y2": ["d", "e", "f"],
...     }
... )
>>> roles = map_roles(df, delimiter="delimiter")
>>> globals().update(roles)
>>> xvars
('x1', 'x2')
>>> yvars
('y1', 'y2')
>>> cs.is_selector(cs_roles.x)
True
>>> cs.is_selector(cs_roles.numy)
True
>>> pl_roles.x.meta.eq(pl.col("x1", "x2"))
True
>>> df.select(pl_roles.numy).columns
['y1']
"""

import polars as pl
import polars.selectors as cs
from boltons.iterutils import split


class _CSRoles:
    """semantic roles of columns in a DataFrame as polars selectors."""

    def __init__(self, xvars: tuple[str], yvars: tuple[str]):
        self.x: cs.Selector = cs.by_name(*xvars)
        self.y: cs.Selector = cs.by_name(*yvars)
        self.numx: cs.Selector = cs.numeric() & self.x
        self.numy: cs.Selector = cs.numeric() & self.y
        self.catx: cs.Selector = cs.categorical() & self.x
        self.caty: cs.Selector = cs.categorical() & self.y


class _PLRoles:
    """semantic roles of columns in a DataFrame as polars expressions."""

    def __init__(self, xvars: tuple[str], yvars: tuple[str], cs_roles: _CSRoles):
        self.x: pl.Expr = pl.col(*xvars)
        self.y: pl.Expr = pl.col(*yvars)
        self.numx: pl.Expr = cs_roles.numx.as_expr()
        self.numy: pl.Expr = cs_roles.numy.as_expr()
        self.catx: pl.Expr = cs_roles.catx.as_expr()
        self.caty: pl.Expr = cs_roles.caty.as_expr()


def map_roles(df: pl.DataFrame, delimiter: str):
    """Assign semantic roles to columns of a DataFrame to obtain polars selectors and expressions.

    Since this relies on the DataFrame's independent and dependent variable columns
    sepearated by a delimiter column. For accurate role assignment use `plutils.cleanup`,
    before instantiating this class or re-order the columns in the DataFrame to have
    all independent variables first, followed by the delimiter column and finally ending
    with the dependent variables.

    """
    xvars, yvars = map(tuple, split(df.columns, delimiter))
    _cs = _CSRoles(xvars, yvars)
    return {
        "xvars": xvars,
        "yvars": yvars,
        "cs_roles": _cs,
        "pl_roles": _PLRoles(xvars, yvars, _cs),
    }
