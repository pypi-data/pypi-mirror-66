# Created by shamilsakib at 7/14/2016

from django.core.management.base import BaseCommand

from django_reporter_pro.controller.query_processor import QueryProcessor
from django_reporter_pro.extensions.handlers.json_handler import JSONHandler
from django_reporter_pro.models import ReportConfiguration


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.requires_model_validation = True

    def handle(self, *args, **options):
        report_config = ReportConfiguration.objects.last()
        headers, query = QueryProcessor.build_query(configuration={
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
            'information': report_config.information,
            'dimensions': report_config.dimensions,
            'measures': report_config.measures,
            'filters': report_config.filters,
            'searches': report_config.searches,
            'report_config': report_config.report_config,
        })
