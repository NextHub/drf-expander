from rest_framework_expander.adapters import get_serializer_adapter
from rest_framework_expander.settings import expander_settings


class ExpanderViewMixin():
    """
    Expander support for views.
    """
    expander_optimizer_class = expander_settings.DEFAULT_OPTIMIZER_CLASS
    expander_parser_class = expander_settings.DEFAULT_PARSER_CLASS

    def get_expander_parser(self, adapter):
        """
        Returns an instance of the expander parser class.
        """
        return self.expander_parser_class(adapter)

    def get_expander_optimizer(self, adapter):
        """
        Returns an instance of the expander optimizer class.
        """
        return self.expander_optimizer_class(adapter)

    def run_expander(self, serializer):
        """
        Runs the expander parser and optimizer.
        """
        adapter = get_serializer_adapter(serializer)

        parser = self.get_expander_parser(adapter)
        adapter.context['expander'] = parser.parse()

        if adapter.many:
            optimizer = self.get_expander_optimizer(adapter)
            adapter.instance = optimizer.optimize()

    def get_serializer(self, *args, **kwargs):
        serializer = super(ExpanderViewMixin, self).get_serializer(*args, **kwargs)
        self.run_expander(serializer)
        return serializer
