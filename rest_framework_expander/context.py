from rest_framework_expander.utils import get_serializer_field_path


class ExpanderContext(object):
    """
    Contains all information related to expander.
    """

    def __init__(self, parent, serializer):
        self.children = dict()
        self.data = dict()
        self.parent = parent
        self.serializer = serializer

    def get_child_by_serializer(self, serializer):
        """
        Returns the expander context for a serializer's field path, or None.
        """
        current = self

        for field_name in get_serializer_field_path(serializer):
            current = current.children.get(field_name)

            if current is None:
                break

        return current
