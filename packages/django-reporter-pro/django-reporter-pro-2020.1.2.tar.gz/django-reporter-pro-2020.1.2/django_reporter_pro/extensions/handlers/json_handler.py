"""
Helper classes for parsers.
"""
from __future__ import unicode_literals

import json

from django.utils.datastructures import ImmutableList


class JSONHandler(json.JSONEncoder):
    def to_json(self, instance, depth=0, expand=None, **kwargs):
        if instance is None:
            return instance
        if type(instance) in [list, ImmutableList]:
            return [self.to_json(_instance, depth=depth, expand=expand) for _instance in instance]
        _result = dict()
        for _attribute in expand:
            if isinstance(_attribute, tuple):
                _result[_attribute[0]] = self.to_json(
                    instance=getattr(instance, _attribute[0], None), depth=depth, expand=_attribute[1]
                )
            else:
                if _attribute == '_python_type':
                    _type = type(instance)
                    _result[_attribute] = _type.__module__ + '.' + _type.__name__
                else:
                    _value = getattr(instance, _attribute, None)
                    if type(_value) in [str, bool, int, float, dict]:
                        _result[_attribute] = _value
                    else:
                        _result[_attribute] = str(_value)
        return _result
