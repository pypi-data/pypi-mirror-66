from json import dumps as _dumps, loads as _loads

from .json_decoder import JsonDecoder as _JsonDecoder
from .json_encoder import JsonEncoder as _JsonEncoder


def from_json(data: str):
    return _loads(data, object_hook=_JsonDecoder.decode)


def to_json(obj: object):
    return _dumps(obj, cls=_JsonEncoder)
