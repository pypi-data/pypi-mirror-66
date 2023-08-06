from django.db.models import F, Sum, Count
from django_reporter_pro.enums.enum_mixin import EnumMixin
from django_reporter_pro.extensions.django.functions.timestamp import DateFromTimeStamp


class AggregateEnum(EnumMixin):
    UN_AGGREGATED = 'unagg'
    COUNT_DISTINCT = 'count'
    COUNT_ALL = 'countall'
    SUM = 'sum'
    AVERAGE = 'average'
    MINIMUM = 'min'
    MAXIMUM = 'max'
    GROUP_DAILY = 'daily'
    GROUP_MONTHLY = 'monthly'


class ProcessMeasure(object):
    @classmethod
    def build_query(cls, model=None, query=None, measures=None, headers=None):
        annotations = {}
        headers = [] if not headers else headers
        for key in measures.keys():
            _measure_field = measures.get(key)
            _measure_config = _measure_field.get('_measure_config')
            _measure = _measure_config.get('aggregation')
            # Adding annotations functions
            _annotation_key = _measure_field.get('query_name') + '_' + _measure
            annotations[_annotation_key] = cls.build_measure_function(
                key=_measure_field.get('name'), measure=_measure)
            # Adding annotations in table values list
            _text = _measure_field.get('verbose_name')
            if _measure_config:
                _text = _measure_config.get('label')
            headers.append({
                "text": _text,
                "value": _annotation_key,
            })
        if annotations:
            query = query.annotate(**annotations)
        return headers, query

    @classmethod
    def build_measure_function(cls, key, measure):
        _function = F(key)
        if measure == AggregateEnum.SUM.value:
            _function = Sum(key)
        elif measure == AggregateEnum.COUNT_ALL.value:
            _function = Count(key)
        elif measure == AggregateEnum.GROUP_DAILY.value:
            _function = DateFromTimeStamp(key, 'YYYY-MM-DD')
        elif measure == AggregateEnum.GROUP_MONTHLY.value:
            _function = DateFromTimeStamp(key, 'YYYY-MM')
        return _function
