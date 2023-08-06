"""Collection of common caching jobs."""

import math
import os.path
import pathlib
import warnings
from typing import IO, AnyStr, Iterator

import requests
from kecleon.base import Clerk, Item


class FileItem(Item):
    """Item interface to file objects."""

    _file: IO[AnyStr]

    def __init__(self, file: IO[AnyStr]) -> None:
        """Initialize a file item."""
        super().__init__()
        self._file = file

    def _get_stream(self) -> Iterator[AnyStr]:
        """Read text from file as a stream."""
        with self._file:
            while True:
                chunk = self._file.read(1024)
                if not chunk:
                    break
                yield chunk

    def _get_all(self) -> AnyStr:
        """Read all text from a file."""
        with self._file:
            return self._file.read()


class FileClerk(Clerk[str]):
    """Clerk for reading from the file system."""

    def __init__(self, bytes: bool = False) -> None:
        super().__init__()
        self._bytes = bytes

    def has_item(self, value: str) -> bool:
        """Verify if the cache has the item."""
        return os.path.isfile(value)

    def get(self, value: str) -> FileItem:
        """Get the item from the cache."""
        return FileItem(open(value, "rb" if self._bytes else "r"))

    def set(self, value: str, item: Item) -> None:
        """Set the cache to the item."""
        dir = pathlib.Path(value).parent
        if not dir.exists():
            dir.mkdir(parents=True, exist_ok=True)
        stream = item.get_stream()
        first = next(stream)
        type = "" if isinstance(first, str) else "b"
        with open(value, "w" + type) as f:
            f.write(first)
            for chunk in stream:
                f.write(chunk)

    def delete(self, value: str) -> None:
        """Delete the item from the cache."""
        if self.has_item(value):
            os.remove(value)

        if os.path.exists(value):
            raise SystemError("Unable to delete " + str(value))  # pragma: no cover
