# coding=utf-8
# Created by shamilsakib at 7/19/2016
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from django_reporter_pro.models import ReportConfiguration


class ReportConfigurationPOSTView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def dispatch(self, request, *args, **kwargs):
        return super(ReportConfigurationPOSTView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise APIException('GET method not allowed.')

    def post(self, request, *args, **kwargs):
        report_config = ReportConfiguration()
        _post_data = request.data
        model_info = _post_data.get('table')
        report_config.model = ContentType.objects.get(
            app_label=model_info.get('app_label'), model=model_info.get('model_name')
        )
        report_config.report_config = _post_data.get('report_config')
        report_config.dimensions = _post_data.get('dimensions')
        report_config.measures = _post_data.get('measures')
        report_config.filters = _post_data.get('filters')
        report_config.searches = _post_data.get('searches')
        report_config.save()
        return JsonResponse(data={
            'uuid': report_config.pk
        })

    def put(self, request, *args, **kwargs):
        report_config = ReportConfiguration.objects.get(pk=kwargs.get('pk'))
        _put_data = request.data
        model_info = _put_data.get('table')
        report_config.model = ContentType.objects.get(
            app_label=model_info.get('app_label'), model=model_info.get('model_name')
        )
        report_config.report_config = _put_data.get('report_config')
        report_config.dimensions = _put_data.get('dimensions')
        report_config.measures = _put_data.get('measures')
        report_config.filters = _put_data.get('filters')
        report_config.searches = _put_data.get('searches')
        report_config.save()
        return JsonResponse(data={
            'uuid': report_config.pk
        })
