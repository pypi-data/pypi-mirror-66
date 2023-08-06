from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from django_reporter_pro.views.report_configuration_get_view import ReportConfigurationGETView
from django_reporter_pro.views.report_configuration_post_view import ReportConfigurationPOSTView
from django_reporter_pro.views.report_configuration_preview import ReportConfigurationPreView
from django_reporter_pro.views.report_models_view import ReportModelView

urlpatterns = [
    path("django-reporter/", TemplateView.as_view(template_name="django_report_pro.html"),
         name="django_report_url", ),
    path("django-reporter-pro/", TemplateView.as_view(template_name="django_reporter_pro.html"),
         name="django_report_pro_url", ),

    url(r'report-model-info/', ReportModelView.as_view(), name='report_model_info'),
    url(r'report-configuration/create', ReportConfigurationPOSTView.as_view(),
        name='report_configuration_create'),
    url(r'report-configuration/update/(?P<pk>(\d{,}))/$', ReportConfigurationPOSTView.as_view(),
        name='report_configuration_update'),
    url(r'report-configuration/detail/(?P<pk>(\d{,}))/$', ReportConfigurationGETView.as_view(),
        name='report_configuration_get'),
    url(r'report-configuration-preview/$', ReportConfigurationPreView.as_view(),
        name='report_configuration_generic_preview'),
    url(r'report-configuration-preview/(?P<pk>(\d{,}))/$', ReportConfigurationPreView.as_view(),
        name='report_configuration_targeted_preview'),
]
