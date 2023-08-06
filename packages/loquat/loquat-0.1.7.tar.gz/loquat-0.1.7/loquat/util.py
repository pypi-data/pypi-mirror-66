import copy
import os
from collections import Iterable
from typing import Any, Dict

unicode_type = str
basestring_type = str

copy_list = (lambda lb: copy(lb) if lb else [])

app_dir = os.path.dirname(os.path.abspath(__name__))

app_pardir = os.path.abspath(os.path.join(app_dir, os.path.pardir))


class ObjectDict(Dict[str, Any]):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)


def list_to_str(value, encode=None):
    """recursively convert list content into string

    :arg list value: The list that need to be converted.
    :arg function encode: Function used to encode object.
    """
    result = []
    for index, v in enumerate(value):
        if isinstance(v, dict):
            result.append(dict_to_str(v, encode))
            continue

        if isinstance(v, list):
            result.append(list_to_str(v, encode))
            continue

        if encode:
            result.append(encode(v))
        else:
            result.append(v)

    return result


def dict_to_str(origin_value, encode=None):
    """recursively convert dict content into string
    """
    value = copy.deepcopy(origin_value)
    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = dict_to_str(v, encode)
            continue

        if isinstance(v, list):
            value[k] = list_to_str(v, encode)
            continue

        if encode:
            value[k] = encode(v)
        else:
            value[k] = v

    return value


def to_str(v, encode=None):
    """convert any list, dict, iterable and primitives object to string
    """
    if isinstance(v, basestring_type):
        return v

    if isinstance(v, dict):
        return dict_to_str(v, encode)

    if isinstance(v, Iterable):
        return list_to_str(v, encode)

    if encode:
        return encode(v)
    else:
        return v


def camel_to_underscore(name):
    """
    convert CamelCase style to under_score_case
    """
    as_list = []
    length = len(name)
    for index, i in enumerate(name):
        if index != 0 and index != length - 1 and i.isupper():
            as_list.append('_%s' % i.lower())
        else:
            as_list.append(i.lower())

    return ''.join(as_list)


def import_object(name: str) -> Any:
    """Imports an object by name.

    ``import_object('x')`` is equivalent to ``import x``.
    ``import_object('x.y.z')`` is equivalent to ``from x.y import z``.

    >>> import tornado.escape
    >>> import_object('tornado.escape') is tornado.escape
    True
    >>> import_object('tornado.escape.utf8') is tornado.escape.utf8
    True
    >>> import_object('tornado') is tornado
    True
    >>> import_object('tornado.missing_module')
    Traceback (most recent call last):
        ...
    ImportError: No module named missing_module
    """
    if name.count(".") == 0:
        return __import__(name)

    parts = name.split(".")
    obj = __import__(".".join(parts[:-1]), fromlist=[parts[-1]])
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])
