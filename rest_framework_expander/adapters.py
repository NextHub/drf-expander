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


class PageExpanderAdapter(ListExpanderAdapter):
    """
    Common interface for list serializers with page number pagination.
    """

    @property
    def instance(self):
        return self.serializer.instance.object_list

    @instance.setter
    def instance(self, instance):
        self.serializer.instance.object_list = instance


class ExpanderAdapterStrategy():
    """
    Returns an instance of the best matching adapter class for serializer.
    """

    def __new__(cls, serializer):
        if isinstance(serializer, ListSerializer):
            if hasattr(serializer.instance, 'object_list'):
                return PageExpanderAdapter(serializer)
            else:
                return ListExpanderAdapter(serializer)

        if isinstance(serializer, Serializer):
            return ExpanderAdapter(serializer)

        raise ExpanderAdapterMissing()
