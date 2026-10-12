"""A module to define semantic roles of columns in a DataFrame."""

import polars as pl
import polars.selectors as cs
from boltons.iterutils import split


class Roles:
    """A class to hold semantic roles of columns in a DataFrame.

    This relies on the DataFrame's independent and dependent variable columns
    sepearated by a delimiter column. For accurate role assignment use `plutils.cleanup`,
    before instantiating this class.
    """

    def __init__(self, df: pl.DataFrame, delimiter: str):
        xvars, yvars = map(tuple, split(df.columns, delimiter))
        self.x = cs.by_name(*xvars)
        self.y = cs.by_name(*yvars)
        self.numx = cs.numeric() & self.x
        self.numy = cs.numeric() & self.y
        self.catx = cs.categorical() & self.x
        self.caty = cs.categorical() & self.y
        self.corner = cs.by_name("Corner")
