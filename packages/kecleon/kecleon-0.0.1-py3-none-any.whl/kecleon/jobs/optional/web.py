"""Collection of common caching jobs."""

import math
import os.path
import warnings
from typing import IO, AnyStr, Iterator

import requests
from kecleon.base import Clerk, Item


class WebItem(Item):
    """Item interface to web resources."""

    def __init__(self, request: requests.Response):
        """Initialize a web item."""
        super().__init__()
        self._request = request

    def _get_stream(self) -> Iterator[AnyStr]:
        """Read text from the web as a stream."""
        return self._request.iter_content()


class WebClerk(Clerk[str]):
    """Clerk for reading from a web resource."""

    def has_item(self, value: str) -> bool:
        """Verify if the cache has the item."""
        try:
            r = requests.get(value, stream=True, allow_redirects=True, timeout=2)
        except requests.exceptions.Timeout:  # pragma: no cover
            return False
        else:
            return r.ok

    def get(self, value: str) -> WebItem:
        """Get the item from the cache."""
        return WebItem(requests.get(value, stream=True, allow_redirects=True))

    def set(self, value: str, item: Item) -> None:
        """Set the cache to the item."""
        raise ValueError("Can't write to web resource")

    def delete(self, value: str) -> None:
        """Delete the item from the cache."""
        raise ValueError("Can't delete web resource")
