from django.apps import apps

from django_reporter_pro.controller.dimension_processor.process_dimensions import ProcessDimension
from django_reporter_pro.controller.filter_processor.process_filters import ProcessFilter
from django_reporter_pro.controller.measure_processor.process_measures import ProcessMeasure

get_model = apps.get_model


class QueryProcessor(object):
    @classmethod
    def build_query(cls, request=None, configuration=None):
        query = None
        if not configuration:
            return query
        model_info = configuration.get('table')
        model = get_model(model_info.get('app_label'), model_info.get('model_name'))
        query = model.objects.all()
        query = ProcessFilter.build_query(
            model=model, request=request, query=query, filters=configuration.get('filters'),
            searches=configuration.get('searches'), search_inputs=configuration.get('search_inputs')
        )
        headers, query = ProcessDimension.build_query(
            query=query, dimensions=configuration.get('dimensions'))
        headers, query = ProcessMeasure.build_query(
            model=model, query=query, measures=configuration.get('measures'), headers=headers)
        return headers, query
