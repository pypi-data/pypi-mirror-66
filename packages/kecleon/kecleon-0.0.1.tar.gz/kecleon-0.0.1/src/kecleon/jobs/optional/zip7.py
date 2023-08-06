"""Collection of common caching jobs."""

import math
import os.path
import warnings
from typing import IO, AnyStr, Iterator, Tuple

import py7zlib
from kecleon.base import Clerk, Item

from ..file import FileClerk
from ..raw import RawItem


class Zip7Clerk(FileClerk):
    """Clerk for reading from a 7z archive."""

    def __init__(self, warn: bool = True) -> None:
        """Initialize a raw item."""
        super().__init__()
        if warn:
            msg = (
                "ZipClerk's underlying datatype does not provide a streaming interface."
            )
            warnings.warn(msg)

    def has_item(self, value: Tuple[str, str]) -> bool:
        """Verify if the cache has the item."""
        if not super().has_item(value[0]):
            return False
        return any(
            member.filename == value[1]
            for member in py7zlib.Archive7z(open(value[0], "rb")).getmembers()
        )

    def get(self, value: str) -> RawItem:
        """Get the item from the cache."""
        member = py7zlib.Archive7z(open(value[0], "rb")).getmember(value[1])
        return RawItem(member.read(), warn=False)

    def set(self, value: Tuple[str, str], item: Item) -> None:
        """Set the cache to the item."""
        return super().set(value[0], item)

    def delete(self, value: str) -> None:
        """Delete the item from the cache."""
        if self.has_item(value):
            os.remove(value[0])

        if os.path.exists(value[0]):
            raise SystemError("Unable to delete " + str(value[0]))  # pragma: no cover
