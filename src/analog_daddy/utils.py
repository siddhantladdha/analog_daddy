"""Miscellaneous utilities."""

from collections.abc import Iterator
from pathlib import Path

import regex as re


def scan_contents(
    contents: bytes | str | Path,
    search_pattern: str,
) -> Iterator[int]:
    r"""Scan contents (lazily if possible) and yields matching line numbers for the given search pattern.

    Parameters
    ----------
    contents : bytes | str | Path
        The contents to scan. Can be a bytes object, a string, or a Path to a file.
    search_pattern : str
        The regex pattern to search for in the contents.

    Returns
    -------
    Iterator[int]
        The line number (1-based) of the first matching line.

    Examples
    --------
    >>> list(
    ...     scan_contents(
    ...         (b"Line 1\nLine 2\nLine 3"),
    ...         r"Line 2",
    ...     )
    ... )
    [2]
    >>> list(
    ...     scan_contents(
    ...         ("Line 1\nLine 2\n Line 3 \n"),
    ...         "^Line 3$",
    ...     )
    ... )
    []
    """
    pattern = re.compile(search_pattern)

    def search(_lines):
        for lineno, line in enumerate(_lines, start=1):
            if pattern.search(line):
                yield lineno

    if isinstance(contents, bytes):
        yield from search(contents.decode().splitlines())
    elif isinstance(contents, str):
        yield from search(contents.splitlines())
    elif isinstance(contents, Path):
        with contents.open() as lines:
            yield from search(lines)
    else:
        raise TypeError(f"Unsupported type: {type(contents)}")
        # TODO: Runtime check needed?
