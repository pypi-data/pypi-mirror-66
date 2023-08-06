class ProcessDimension(object):
    @classmethod
    def build_query(cls, query=None, dimensions=None):
        _values = []
        _headers = []
        for key in dimensions.keys():
            _dimension_field = dimensions.get(key)
            _display_config = _dimension_field.get('_display_config')
            # Adding dimensions as query VALUES fields
            _field_key = _dimension_field.get('query_name')
            _values.append(_field_key)
            # Populating dimension display detail
            _text = _dimension_field.get('verbose_name')
            if _display_config:
                _text = _display_config.get('label')
            _headers.append({
                "text": _text,
                "value": _field_key,
            })
        query = query.values(*_values)
        return _headers, query
