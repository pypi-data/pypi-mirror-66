"""Collection of common caching jobs."""

import math
import os.path
import warnings
from typing import IO, AnyStr, Iterator

import requests
from kecleon.base import Clerk, Item


class RawItem(Item):
    """
    Item interface for raw text.

    This is useful if you need to update the cache externally.
    """

    _text: AnyStr

    def __init__(self, text: AnyStr, warn: bool = True) -> None:
        """Initialize a raw item."""
        super().__init__()
        self._text = text
        if warn:
            msg = (
                "RawItem's underlying datatype does not provide a streaming interface."
            )
            warnings.warn(msg)

    def _get_stream(self) -> Iterator[AnyStr]:
        """Get raw text as a stream."""
        for i in range(int(math.ceil(len(self._text) / 1024))):
            yield self._text[i * 1024 : (i + 1) * 1024]

    def _get_all(self) -> AnyStr:
        """Get raw text."""
        return self._text
