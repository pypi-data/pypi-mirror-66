from enum import Enum

from django_reporter_pro.extensions.basic.stringification import camel_to_title


class EnumMixin(Enum):

    @classmethod
    def get_choices(cls):
        return [(enum.value, camel_to_title(enum.value)) for enum in cls]

    @classmethod
    def get_select_choices(cls):
        return [{'key': enum.value, 'text': camel_to_title(enum.value)} for enum in cls]
