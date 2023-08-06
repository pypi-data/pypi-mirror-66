"""Collection of common caching jobs."""

from .file import FileClerk, FileItem
from .raw import RawItem

try:
    from .optional.web import WebClerk, WebItem
except ImportError:
    pass

try:
    from .optional.zip7 import Zip7Clerk
except ImportError:
    pass
