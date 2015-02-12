def get_serializer_path(serializer, attribute):
    """
    Returns all values of attribute from the root serializer to serializer.
    """
    path = list()
    current = serializer

    while getattr(current, attribute, None):
        value = getattr(current, attribute)
        path.append(value)
        current = current.parent

    path.reverse()
    return path


def get_serializer_field_path(serializer):
    """
    Returns all values of field_name from the root serializer to serializer.
    """
    return get_serializer_path(serializer, 'field_name')


def get_serializer_source_path(serializer):
    """
    Returns all values of source from the root serializer to serializer.
    """
    return get_serializer_path(serializer, 'source')
