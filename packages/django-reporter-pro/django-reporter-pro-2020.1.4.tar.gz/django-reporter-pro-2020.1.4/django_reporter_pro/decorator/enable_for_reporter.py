# Created by shamilsakib


def enable_for_reporter(**kwargs):
    registry = {}

    def enable_reporter(_api_view):
        if '_params' in dir(_api_view):
            if _api_view.__name__ not in _api_view._params:
                _api_view._params[_api_view.__name__] = dict()
            _api_view._params[_api_view.__name__]['enable_for_reporter'] = dict(**kwargs)
        else:
            registry[_api_view.__name__] = dict()
            registry[_api_view.__name__]['enable_for_reporter'] = dict(**kwargs)
            _api_view._params = registry
        return _api_view

    return enable_reporter
