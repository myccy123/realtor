# -*- coding: utf-8 -*-
import json
from datetime import datetime
from decimal import Decimal


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return datetime.strftime(obj, '%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, obj)


def dumps(dic, cls=None):
    return json.dumps(dic, indent=2, ensure_ascii=False,
                      cls=MyEncoder if cls is None else cls)


def loads(s):
    if isinstance(s, bytes):
        return json.loads(s.decode())
    return json.loads(s)


def pretty(s):
    return dumps(loads(s))
