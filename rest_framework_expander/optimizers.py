from rest_framework_expander import utils


class ExpanderOptimizer():
    """
    Optimizes querysets for inline expansion.
    """

    def __init__(self, adapter):
        self.adapter = adapter

    def optimize(self):
        instance = self.adapter.instance
        expander = self.adapter.context['expander']

        for descendant in expander.walk():
            instance = self.fallback_expand(instance, descendant)

        return instance

    def fallback_expand(self, instance, expander):
        return instance


class PrefetchRelatedOptimizer(ExpanderOptimizer):
    """
    Optimizer which falls back on prefetch related.
    """

    def fallback_expand(self, instance, expander):
        if hasattr(instance, 'model'):
            source_path = utils.get_serializer_source_path(expander.serializer)
            source_name = utils.get_model_source_name(source_path, instance.model)

            if source_name:
                instance = instance.prefetch_related(source_name)

        return instance


class SelectRelatedOptimizer(ExpanderOptimizer):
    """
    Optimizer which falls backs on select related.
    """

    def fallback_expand(self, instance, expander):
        if hasattr(instance, 'model'):
            source_path = utils.get_serializer_source_path(expander.serializer)
            source_name = utils.get_model_source_name(source_path, instance.model)

            if source_name:
                instance = instance.select_related(source_name)

        return instance
