from rest_framework.serializers import ListSerializer, Serializer

from rest_framework_expander.exceptions import ExpanderAdapterMissing


class ExpanderAdapter():
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
    def many(self):
        return False


class ListExpanderAdapter(ExpanderAdapter):
    """
    Common interface for list serializers.
    """

    @property
    def object_serializer(self):
        return self.serializer.child

    @property
    def many(self):
        return True




class ExpanderAdapterStrategy():
    """
    Returns an instance of the best matching adapter class for serializer.
    """

    def __new__(cls, serializer):
        if isinstance(serializer, ListSerializer):
            return ListExpanderAdapter(serializer)

        if isinstance(serializer, Serializer):
            return ExpanderAdapter(serializer)

        raise ExpanderAdapterMissing()
