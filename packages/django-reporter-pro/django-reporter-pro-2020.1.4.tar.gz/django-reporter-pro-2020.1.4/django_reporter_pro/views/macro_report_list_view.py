# coding=utf-8
# Created by shamilsakib at 7/19/2016
from django.http.response import JsonResponse
from django_reporter_pro.models import ReportConfiguration
from rest_framework.exceptions import APIException
from rest_framework.views import APIView


class MacroReportListGETView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def dispatch(self, request, *args, **kwargs):
        return super(MacroReportListGETView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        macro_reports = ReportConfiguration.objects.filter(
            information__has_key='is_macro', information__is_macro=True)
        return JsonResponse(data={
            "results": [{
                'text': _macro.information.get('title') if _macro.information else _macro.pk,
                'value': _macro.pk
            } for _macro in macro_reports]
        })

    def post(self, request, *args, **kwargs):
        raise APIException('POST method not allowed.')
