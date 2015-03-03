from collections import OrderedDict
from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'REST_FRAMEWORK_EXPANDER', dict())

DEFAULTS = {
    'COLLAPSED_FIELDS': OrderedDict((
        ('id', 'rest_framework_expander.fields.CollapsedIdentityField'),
        ('url', 'rest_framework_expander.fields.CollapsedHyperlinkField'),
    )),
    'DEFAULT_EXPANDED': True,
    'DEFAULT_PARSER_CLASS': 'rest_framework_expander.parsers.ExpanderParser',
    'DEFAULT_OPTIMIZER_CLASS': 'rest_framework_expander.optimizers.PrefetchExpanderOptimizer',
    'EXPANSION_KEY': 'expand',
    'EXPANSION_ITEM_SEPARATOR': ',',
    'EXPANSION_PATH_SEPARATOR': '.',
    'FAIL_ON_DEPTH_BREACHED': False,
    'FAIL_ON_FIELD_MISSING': False,
    'MAX_DEPTH': 1,
}

IMPORT_STRINGS = (
    'DEFAULT_PARSER_CLASS',
    'DEFAULT_OPTIMIZER_CLASS',
)


expander_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
