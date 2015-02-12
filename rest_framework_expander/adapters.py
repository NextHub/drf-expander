from rest_framework.pagination import BasePaginationSerializer
from rest_framework.serializers import ListSerializer, Serializer

from rest_framework_expander.exceptions import ExpanderAdapterMissing


class SerializerAdapter():
    """
    Common interface for serializers.
    """

    def __init__(self, serializer):
        self._serializer = serializer

    @property
    def context(self):
        return self.serializer.context

    @property
    def fields(self):
        return self.object_serializer.fields

    @property
    def instance(self):
        return self.serializer.instance

    @instance.setter
    def instance(self, instance):
        self.serializer.instance = instance

    @property
    def serializer(self):
        return self._serializer

    @property
    def object_serializer(self):
        return self.serializer

    @property
    def root(self):
        return self.serializer.root

    @property
    def many(self):
        return False


class ListSerializerAdapter(SerializerAdapter):
    """
    Common interface for list serializers.
    """

    @property
    def object_serializer(self):
        return self.serializer.child

    @property
    def many(self):
        return True


class PaginationSerializerAdapter(SerializerAdapter):
    """
    Common interface for pagination serializers.
    """

    @property
    def instance(self):
        return self.serializer.instance.object_list

    @instance.setter
    def instance(self, instance):
        self.serializer.instance.object_list = instance

    @property
    def object_serializer(self):
        results_field = self.serializer.results_field
        return self.serializer.fields[results_field].child

    @property
    def many(self):
        return True


ADAPTER_MAPPING = (
    (BasePaginationSerializer, PaginationSerializerAdapter),
    (ListSerializer, ListSerializerAdapter),
    (Serializer, SerializerAdapter),
)


def get_serializer_adapter(serializer, mapping=ADAPTER_MAPPING):
    """
    Returns the best matching adapter for serializer.
    """
    for serializer_class, adapter_class in mapping:
        if isinstance(serializer, serializer_class):
            return adapter_class(serializer)

    raise ExpanderAdapterMissing()
