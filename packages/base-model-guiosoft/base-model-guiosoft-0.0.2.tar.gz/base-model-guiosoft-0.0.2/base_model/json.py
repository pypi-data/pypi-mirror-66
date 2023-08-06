from orjson import dumps as _dumps
from orjson import loads as _loads


def loads(obj):
    """ Deserialize JSON to python objects using orjson """
    return _loads(obj)


def dumps(obj):
    """ Serialize Python object to JSON using orjson """
    return _dumps(obj, default=str).decode('utf-8')
