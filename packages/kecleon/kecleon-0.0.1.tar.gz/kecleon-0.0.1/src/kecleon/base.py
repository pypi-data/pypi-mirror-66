"""
Base interfaces to add custom transformations.

A :class:`Item` is a small interface wrapping an underlying object.
It can only return text or an iterator of text. The underlying object
can be anything such as a string, bytes, file or HTTP object.
The underlying object doesn't matter as a subclass will bind it
correctly to the interface.

A :class:`Clerk` is a job that the cache can perform. For example
downloading a web file, extracting an archive or reading from the
file system.
"""

import abc
from typing import AnyStr, Generic, Iterator, TypeVar

T = TypeVar("T")


class Item:
    """
    An abstract interface to provide a layer of compatibly over raw objects.

    This provides two interfaces to interact with the containing data.

    1.  A stream interface, to allow interactions with large files.
    2.  A non-stream interface, to allow convenient interactions with
        the data.

    This only returns strings or bytes. This is because parsing should
    happen after the procurement of raw data happens.
    """

    def __init__(self):
        """Initialize item."""
        self._consumed = False

    def get_stream(self) -> Iterator[AnyStr]:
        """
        Get data as a stream.

        Internally we only uses this interface. This is because
        some files can exceed the amount of ram a computer has
        available. When this happens the computer can grind to a halt
        and prevent any and all interactions with the system. To fix
        this will require a potentially dangerous hard reboot.

        When overriding this method it's highly recommended to always
        use a streaming interface if available. Sometimes this is
        not possible in which case notifying the user at creation of
        the object is recommended.

        This method ensures that the data is only read once. Since
        streams should be the primary interface and getting the same
        stream twice is not always possible this method can only be
        called once. This should not be overridden by subclasses
        unless the subclass ensures that either :meth:`get_all` or
        :meth:`get_stream` are called a maximum of once.

        :returns: Chunked segments of the desired text.
        """
        if self._consumed:
            raise ValueError("{} has already been consumed".format(type(self).__name__))
        self._consumed = True
        return self._get_stream()

    @abc.abstractmethod
    def _get_stream(self) -> Iterator[AnyStr]:
        """
        Get data as a stream.

        This is the internal method for :meth:`get_stream`.
        It is what gets the stream from the internal object.

        :returns: Chunked segments of the desired text.
        """
        ...  # pragma: no cover

    def get_all(self) -> AnyStr:
        """
        Get data as a string or bytes.

        This reads the entire string or bytes into memory. Returning
        the entire value at once. This is normally the more convenient
        method to interact with. But it can break on larger files.

        By default this interface just combines all the data from the
        stream interface into one string.

        This method ensures that the data is only read once. Since
        streams should be the primary interface and getting the same
        stream twice is not always possible this method can only be
        called once. This should not be overridden by subclasses
        unless the subclass ensures that either :meth:`get_all` or
        :meth:`get_stream` are called a maximum of once.

        :returns: The entire desired text.
        """
        if self._consumed:
            raise ValueError("{} has already been consumed".format(type(self).__name__))
        self._consumed = True
        return self._get_all()

    def _get_all(self) -> AnyStr:
        """
        Get data as a string or bytes.

        This is the internal method for :meth:`get_all`.
        It is what gets the text from the internal object.

        :returns: The entire desired text.
        """
        stream = self._get_stream()
        first = next(stream)
        sep = "" if isinstance(first, str) else b""
        return first + sep.join(stream)


class Clerk(Generic[T], abc.ABC):
    """
    Interface for managing caches.

    Each method take at least one value which with most Kecleon
    defined Clerks will be a string. This will be the location to the
    file that we need to interact with. Such as the location on disk
    or the location on the web.

    Ultimately the ``value`` can be anything that you allow to
    identify the cache. For example a custom cache could be passed a
    tuple of the source and destination.
    """

    def __eq__(self, other: object) -> bool:
        """Compare if two clerks are the same."""
        # We are testing if the type is the same. Not if they are a
        # clerk. We are also not testing for subclasses.
        return type(self) is type(other)

    @abc.abstractmethod
    def has_item(self, value: T) -> bool:
        """Verify if the cache contains the item."""
        ...  # pragma: no cover

    @abc.abstractmethod
    def get(self, value: T) -> Item:
        """Get the item from the cache."""
        ...  # pragma: no cover

    @abc.abstractmethod
    def set(self, value: T, item: Item) -> None:
        """
        Set the cache to the item.

        To prevent the system crashing when reading large files,
        please always use the stream interface that the
        :class:`base.Item` exposes.
        """
        ...  # pragma: no cover

    @abc.abstractmethod
    def delete(self, value: T) -> None:
        """Delete the item from the cached."""
        ...  # pragma: no cover
