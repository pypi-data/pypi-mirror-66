from django.db.backends.postgresql.operations import DatabaseOperations
from django.db.models import DateField
from django.db.models.lookups import (
    Transform, )


# EXTRACT(\'month\' FROM T2."date_of_birth") AS "month"
# TO_CHAR(TO_TIMESTAMP({0}::float/1000), \'YYYY-MM-DD\')


class ExtendedDatabaseOperations(DatabaseOperations):

    def timestamp_extract_date(self, field_name, date_format):
        # https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT
        return "TO_CHAR(TO_TIMESTAMP({0}::float/1000), \'{1}\')".format(field_name, date_format)


class DateFromTimeStamp(Transform):
    output_field = DateField()
    date_format = 'YYYY-MM-DD'

    def __init__(self, expression, date_format, **extra):
        super().__init__(expression, **extra)
        self.date_format = date_format

    def as_sql(self, compiler, connection):
        sql, params = compiler.compile(self.lhs)
        sql = ExtendedDatabaseOperations(connection=connection).timestamp_extract_date(
            field_name=sql, date_format=self.date_format)
        return sql, params

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        copy = super().resolve_expression(query, allow_joins, reuse, summarize, for_save)
        return copy
