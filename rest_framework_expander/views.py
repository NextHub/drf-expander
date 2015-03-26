from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_expander.settings import expander_settings


class ExpanderViewMixin(object):
    """
    Expander support for views.
    """
    expander_adapter_class = expander_settings.DEFAULT_ADAPTER_CLASS
    expander_optimizer_class = expander_settings.DEFAULT_OPTIMIZER_CLASS
    expander_parser_class = expander_settings.DEFAULT_PARSER_CLASS

    def get_expander_adapter(self, serializer):
        """
        Returns an instance of the expander adapter class.
        """
        return self.expander_adapter_class(serializer)

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
        Runs the expander parser.
        """
        adapter = self.get_expander_adapter(serializer)
        parser = self.get_expander_parser(adapter)
        adapter.context['expander'] = parser.parse()

    def get_serializer(self, *args, **kwargs):
        serializer = super(ExpanderViewMixin, self).get_serializer(*args, **kwargs)
        self.run_expander(serializer)
        return serializer


class ExpanderListModelMixin(ExpanderViewMixin):
    """
    Provides a generic list view with expander optimizations.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        adapter = self.get_expander_adapter(serializer)
        optimizer = self.get_expander_optimizer(adapter)

        queryset = optimizer.to_optimized_queryset(queryset)
        page = self.paginate_queryset(queryset)

        adapter.instance = list(page if page is not None else queryset)

        if adapter.instance:
            adapter.instance = optimizer.to_optimized_objects(adapter.instance)

        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)


class ExpanderListAPIView(ExpanderListModelMixin, GenericAPIView):
    """
    Provides a list API view with expander optimizations.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
