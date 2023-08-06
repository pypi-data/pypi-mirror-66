# coding=utf-8
# Created by shamilsakib at 7/19/2016
from django.http.response import JsonResponse
from rest_framework.views import APIView

from django_reporter_pro.extensions.handlers.json_handler import JSONHandler


class ModelJsonHandlerView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def dispatch(self, request, *args, **kwargs):
        return super(ModelJsonHandlerView, self).dispatch(request, *args, **kwargs)

    def get_json(self, request, data, expand=[], *args, **kwargs):
        if not isinstance(data, dict):
            data = {'results': JSONHandler().to_json(data, depth=2, expand=expand)}
        return JsonResponse(data)

    def post_json(self, request, data, *args, **kwargs):
        return JsonResponse(data)

    def get(self, request, *args, **kwargs):
        return self.get_json(request, data={}, expand=[], *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.post_json(request, {}, *args, **kwargs)
