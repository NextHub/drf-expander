from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ForeignKey


def get_serializer_path(serializer, attribute):
    """
    Returns all values of attribute from the root serializer to serializer.
    """
    path = list()
    current = serializer

    while current:
        value = getattr(current, attribute, None)

        if value and not hasattr(current.parent, 'child'):
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


def get_model_source_name(source_path, model):
    """
    Returns a verified model source name, or None.
    """
    meta = model._meta

    for source in source_path:
        try:
            field = meta.get_field(source)
        except FieldDoesNotExist:
            return None

        if isinstance(field, ForeignKey):
            meta = field.rel.to._meta
        else:
            return None

    return '__'.join(source_path)
