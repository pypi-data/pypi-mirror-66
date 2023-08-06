# coding=utf-8
# Created by shamilsakib at 7/19/2016
from django.http.response import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from django_reporter_pro.controller.query_processor import QueryProcessor
from django_reporter_pro.extensions.handlers.json_handler import JSONHandler
from django_reporter_pro.models import ReportConfiguration


class ReportConfigurationPreView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def dispatch(self, request, *args, **kwargs):
        return super(ReportConfigurationPreView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise APIException('GET method not allowed.')

    def post(self, request, *args, **kwargs):
        post_data = request.data
        headers, query = QueryProcessor.build_query(configuration=post_data)
        return JsonResponse(data={
            'headers': headers,
            'results': list(query),
        })

    def put(self, request, *args, **kwargs):
        report_config = ReportConfiguration.objects.get(pk=kwargs.get('pk'))
        search_inputs = request.data
        configuration = {
            'table': JSONHandler().to_json(
                report_config.model.model_class(), depth=2,
                expand=[(
                    '_meta', [
                        'label', 'app_label', 'model_name', 'object_name', 'db_table', 'installed',
                        'abstract', 'proxy', 'auto_created',
                        ('pk', ['column', 'verbose_name']),
                    ],
                )]
            ).get('_meta'),
            'report_config': report_config.report_config,
            'dimensions': report_config.dimensions,
            'measures': report_config.measures,
            'filters': report_config.filters,
            'searches': report_config.searches,
            'search_inputs': search_inputs,
        }
        headers, query = QueryProcessor.build_query(request=request, configuration=configuration)
        return JsonResponse(data={
            'headers': headers,
            'results': list(query),
        })
