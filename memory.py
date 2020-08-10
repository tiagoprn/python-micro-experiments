# extracted from here: https://rednafi.github.io/digressions/python/2020/07/03/python-mixins.html

from collections.abc import Mapping, Container
from sys import getsizeof


def deep_getsizeof(o: object, ids: None = None) -> int:
    """Find the memory footprint of a Python object.

    This is a recursive function that drills down a Python object graph
    like a dictionary holding nested dictionaries with lists of lists
    and tuples and sets.

    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.

    To manually call the garbage collector, you can use:

    import gc
    gc.collect()

    Params
    ------
     o: object
        The object
     ids: None
        Later an iterable is assigned to store the object ids

     Returns
     --------
     int
        Returns the size of object in bytes
    """

    if ids is None:
        ids = set()

    d = deep_getsizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str):
        return r

    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())

    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)

    return r
