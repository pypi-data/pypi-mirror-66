from django.db.models import Q
from django_reporter_pro.enums.enum_mixin import EnumMixin


class FilterTypeEnum(EnumMixin):
    EQUAL = 'eq'
    NOT_EQUAL = 'neq'
    IN = 'in'
    NOT_IN = 'not_in'
    LIKE = 'like'
    NOT_LIKE = 'not_like'
    LIKE_CASE_INS = 'ilike'
    NOT_LIKE_CASE_INS = 'not_ilike'
    GREATER_THAN = 'gt'
    GREATER_THAN_EQUAL = 'gte'
    LESS_THAN = 'lt'
    LESS_THAN_EQUAL = 'lte'
    BETWEEN_INCLUSIVE = 'numbti'
    IS_NULL = 'is_null'
    NOT_NULL = 'not_null'


class ProcessFilter(object):
    @classmethod
    def build_query(cls, model=None, request=None, query=None, filters=None, searches=None, search_inputs=None):
        _filter_queries = None
        if model and hasattr(model, 'provide_reporter_pro_query_request'):
            query = getattr(model, 'provide_reporter_pro_query_request')(model=model, request=request, query=query)
        for _and_filters in filters:
            _and_queries = None
            for key in _and_filters.keys():
                _filter = _and_filters.get(key)
                _filter_key = _filter.get('query_name')
                _filter_query = cls.get_q_expression(key=_filter_key, config=_filter.get('_filter_config'))
                _and_queries = _filter_query if not _and_queries else _and_queries & _filter_query
            if _and_queries:
                _filter_queries = _and_queries if not _filter_queries else _filter_queries | Q(_and_queries)
        _search_queries = cls.build_search_query(searches=searches, search_inputs=search_inputs)
        if _search_queries:
            _filter_queries = _search_queries if not _filter_queries else _filter_queries & _search_queries
        if _filter_queries:
            query = query.filter(_filter_queries)
        return query

    @classmethod
    def build_search_query(cls, searches=None, search_inputs=None):
        if not search_inputs:
            return None
        _search_queries = None
        for _key in searches.keys():
            _values = search_inputs.get(_key)
            if not _values:
                continue
            _search = searches.get(_key)
            _search_key = _search.get('query_name')
            _or_queries = None
            for _val in _values.split(','):
                _query = Q(**{_search_key + '__icontains': _val})
                _or_queries = _query if not _or_queries else _or_queries | _query
            if _or_queries:
                _search_queries = _or_queries if not _search_queries else _search_queries & Q(_or_queries)
        return _search_queries

    @classmethod
    def get_q_expression(cls, key, config):
        _query = Q()
        filter_type = config.get('filter')
        filter_inputs = config.get('filterInputs')
        _query_dict = {}
        if filter_type == FilterTypeEnum.BETWEEN_INCLUSIVE.value:
            _query_dict[key + '__gte'] = float(filter_inputs[0])
            _query_dict[key + '__lte'] = float(filter_inputs[1])
            _query = Q(**_query_dict)
        elif filter_type == FilterTypeEnum.GREATER_THAN.value:
            _query_dict[key + '__gt'] = float(filter_inputs[0])
            _query = Q(**_query_dict)
        elif filter_type == FilterTypeEnum.EQUAL.value:
            _query_dict[key] = filter_inputs[0]
            _query = Q(**_query_dict)
        return _query
