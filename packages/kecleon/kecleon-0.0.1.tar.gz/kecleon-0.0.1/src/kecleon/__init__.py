"""
Kecleon; cacheing through a simple store interface.

The design is based on a store where you only interact with one clerk.
That clerk then goes off to get the items that you desire.
This is similar to `Argos' <https://en.wikipedia.org/wiki/Argos_(retailer)>`_
model for customer service.

The clerk at the front desk only checks the warehouse for the item you
want. If it's not in the warehouse then they can check with a
deliveries clerk if there are any that have yet to be unpacked.
Finally if it's not in deliveries then a transport clerk will be asked
to get the product from another store into the current one. Finally if
none are available then you'll be instructed to come back another time.

This contrived example can be easily mapped to this library. The first
clerk could be a :class:`jobs.FileClerk`, the deliveries clerk can be
a :class:`jobs.Zip7Clerk` and finally the transport clerk can be a
:class:`jobs.WebClerk`.

After defining how the store moves goods internally, we can focus on
where each item comes from. The good we want could be always be stored
in aisle 1, shelf 2. It's deliveries stored in deliveries section A
and finally always come from strore #2.

In our example the item we want is post information, :code:`Posts.xml`.
It's stored in the following archive :code:`codereview.stackexchange.com.7z`
and is available from :code:`https://archive.org/download/stackexchange/codereview.stackexchange.com.7z`.

This would be simple to build with Kecleon.

.. testcode ::

    from kecleon import Store, FileClerk, WebClerk
    from kecleon.jobs import Zip7Clerk

    store = Store(
        warehouse=FileClerk(),
        deliviers=Zip7Clerk(),
        provider=WebClerk(),
    )

    posts = store.get(
        warehouse='.cache/codereview/Posts.xml',
        deliviers=('.cache/codereview/codereview.stackexchange.com.7z', 'Posts.xml'),
        provider='https://archive.org/download/stackexchange/codereview.stackexchange.com.7z',
    )

A lot of the terminology maps to store related terms.

Clerk
    An object that inherits from :class:`base.Clerk` and interacts
    with their department's items.

Department
    Each clerk works in a set department. In the above example the
    :class:`jobs.FileClerk` works in the ``warehouse`` department.

Location / Item
    This is the location of the item. To be able to function properly
    clerks and departments needs to know where the item's location is.

Kecleon allows importing some of the most common clerks from the top
level package. Some clerks it doesn't include. These are accessible
from the :mod:`kecleon.jobs` module. If this doesn't include a clerk
you need then you can build your own by extending the objects in
:mod:`kecleon.base`.
"""

from .base import Clerk, Item
from .jobs import FileClerk, WebClerk
from .store import Store

__all__ = [
    "Clerk",
    "FileClerk",
    "Item",
    "Store",
    "WebClerk",
]
