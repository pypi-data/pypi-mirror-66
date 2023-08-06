"""
Store cache interface.

There are three different but linked classes here.
It's recomended to only use :class:`Store` when using Kecleon.
This is as it supplies some convenience methods for building both the
intermerry :class:`Clerks` and final :class:`Line`.

If :class:`Store` doesn't supply the interface that you want then you
should look into subclassing :class:`Line` or writing your own store front.
"""

import abc
import collections.abc
import inspect
from typing import Any, Dict, Iterator, List, Tuple, Union

from .base import Clerk, Item


class Clerks:
    """Helper class to ease storage of clerks and departments."""

    clerks: Dict[str, Clerk]
    signature: inspect.Signature

    def __init__(self, clerks: Dict[str, Clerk]) -> None:
        """Initalize Clerks."""
        self.clerks = clerks
        self.signature = self._build_signature(list(clerks))

    @staticmethod
    def _build_signature(clerks: Dict[str, Clerk]) -> inspect.Signature:
        """Build a signature to build the line from."""
        return inspect.Signature(
            [
                inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                for name in clerks
            ]
        )

    def line(self, *args: Any, **kwargs: Any) -> "Line":
        """Build a :class:`Line` with the provided department locations."""
        return Line(self.clerks, self.signature.bind(*args, **kwargs).arguments)


SubList = Tuple[str, Any, Clerk]


class Line:
    """
    The line that an item travel through to get to the buyer.

    This contains the clerk, department and item's location for the
    entire supply line of one item.
    """

    clerks: Dict[str, Clerk]
    departments: Dict[str, Any]

    def __init__(self, clerks: Dict[str, Clerk], departments: Dict[str, Any]) -> None:
        """Initalize Line."""
        self.clerks = clerks
        self.departments = departments

    def __iter__(self) -> Iterator[SubList]:
        """Iterate line."""
        return iter(
            (name, self.departments[name], clerk) for name, clerk in self.clerks.items()
        )

    def __reversed__(self) -> Iterator[SubList]:
        """Iterate line in reverse."""
        return iter(
            (name, self.departments[name], clerk)
            for name, clerk in reversed(self.clerks.items())
        )

    def get(self) -> Item:
        """
        Get value from the store's line.
        
        This does not take any arguments, as the line has already been
        defined. It just walks until it finds a hit and then walks
        back adding the item to all the other locations.
        """
        sub_line = iter(self._get_sub_line())
        _, department, clerk = next(sub_line)
        return self._update(sub_line, clerk.get(department))

    def set(self, **kwarg: Item) -> Item:
        """
        Set a department to an item.
        
        This takes only one keyword argument of the department to
        update. Setting more than one wouldn't make sense as this
        updates all the departments automatically.
        """
        if len(kwarg) != 1:
            raise TypeError("must be supplied one keyword argument")
        ((name, value),) = kwarg.items()
        sub_line = self._get_from(name)
        _, department, clerk = next(sub_line)
        clerk.set(department, value)
        return self._update(sub_line, clerk.get(department))

    def delete(self, name: str) -> None:
        """
        Delete the stored item from the provided department.

        Specifying a department further down the line, or even the end
        of the line, will cause all the departments up the line to
        delete their storage.
        """
        sub_line = self._get_from(name)
        for _, department, clerk in sub_line:
            clerk.delete(department)

    def _update(self, sub_line: Iterator[SubList], value: Item) -> Item:
        """Update the provided departments."""
        for _, department, clerk in sub_line:
            clerk.set(department, value)
            value = clerk.get(department)
        return value

    def _get_sub_line(self) -> List[SubList]:
        """Get the sub line to the first cached department."""
        values = list(self)
        for i, (_, department, clerk) in enumerate(values):
            if clerk.has_item(department):
                break
        else:
            raise ValueError("Item is unavailable")
        return values[i::-1]

    def _get_from(self, name: str) -> Iterator[SubList]:
        """Get the sub line from the provided department."""
        if name not in self.clerks:
            raise TypeError("got an unexpected keyword argument: " + name)
        reverse = reversed(self)
        for name_, department, clerk in reverse:
            if name_ == name:
                yield name_, department, clerk
                break
        yield from reverse


class Store:
    """
    The Kecleon store interface.

    Build a store with a selection of :class:`kecleon.base.Clerk`\ s. And
    easily get data from the supply line.

    Data can be supplied as a mix of a dictionary and keyword
    arguments. The order of the departments and clerks are important
    when initializing the store. Afterwards they can be supplied in
    any order.
    """

    clerks: Clerks

    def __init__(
        self, clerks: Union[Clerks, Dict[str, Clerk]] = None, **kwargs: Clerk
    ) -> None:
        """Initialize store."""
        if clerks is None:
            clerks = {}
        if clerks and kwargs:
            if not isinstance(clerks, collections.abc.Mapping):
                clerks = clerks.clerks
            clerks = {**clerks, **kwargs}
        else:
            clerks = clerks or kwargs
        if isinstance(clerks, collections.abc.Mapping):
            self.clerks = Clerks(clerks)
        else:
            self.clerks = clerks

    def get(self, *args: Any, **kwargs: Any) -> Item:
        """Get an item from the supplied locations."""
        return self.line(*args, **kwargs).get()

    def line(self, *args: Any, **kwargs: Any) -> Line:
        """Get the supply line for the supplied locations."""
        return self.clerks.line(*args, **kwargs)
