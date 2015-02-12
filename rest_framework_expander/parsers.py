from rest_framework.serializers import Serializer

from rest_framework_expander.context import ExpanderContext
from rest_framework_expander.exceptions import ExpanderFieldMissing, ExpanderDepthBreached
from rest_framework_expander.settings import expander_settings


class ExpanderParser():
    """
    Parses the expander query parameters.
    """
    expansion_key = expander_settings.EXPANSION_KEY
    expansion_item_separator = expander_settings.EXPANSION_ITEM_SEPARATOR
    expansion_path_separator = expander_settings.EXPANSION_PATH_SEPARATOR
    fail_on_depth_breached = expander_settings.FAIL_ON_DEPTH_BREACHED
    fail_on_field_missing = expander_settings.FAIL_ON_FIELD_MISSING
    max_depth = expander_settings.MAX_DEPTH

    def __init__(self, adapter):
        self.adapter = adapter

    def parse(self):
        """
        Returns the root expander context by parsing the query parameters.
        """
        root = ExpanderContext(None, None)

        request = self.adapter.context['request']
        param = request.QUERY_PARAMS.get(self.expansion_key, '')

        for item in param.split(self.expansion_item_separator):
            parts = item.split(self.expansion_path_separator, self.max_depth + 1)

            if self.max_depth < len(parts):
                if self.fail_on_depth_breached:
                    raise ExpanderDepthBreached()
                else:
                    parts = parts[:self.max_depth]

            serializer = self.adapter.object_serializer
            node = root

            for part in parts:
                if not isinstance(serializer.fields.get(part), Serializer):
                    if self.fail_on_field_missing:
                        raise ExpanderFieldMissing()
                    else:
                        break

                serializer = serializer.fields[part]

                if part not in node.children:
                    node.children[part] = ExpanderContext(node, serializer)

                node = node.children[part]

        return root
