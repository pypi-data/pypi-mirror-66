import re

NORMALIZER_ONE = re.compile('(.)([A-Z][a-z]+)')
NORMALIZER_TWO = re.compile('([a-z0-9])([A-Z])')


def camel_to_title(name):
    """Generate display from a model name of joined words"""
    name1 = NORMALIZER_ONE.sub(r'\1_\2', name)
    name2 = NORMALIZER_TWO.sub(r'\1_\2', name1)
    title = "".join([a if a.isupper() else b for a, b in zip(name2, name2.title())])
    return title.replace(r'_', r' ')
