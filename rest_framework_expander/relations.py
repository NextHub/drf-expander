from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import ForeignKey


class PKObject(object):
    """
    Mock object for partial instances.

    Provides primary key and model meta.
    """

    def __init__(self, parent, field_name):
        field = parent._meta.get_field(field_name)

        if isinstance(field, ForeignKey):
            target_field = field
            target_meta = field.rel.to._meta

        elif isinstance(field, GenericForeignKey):
            content_type_field = parent._meta.get_field(field.ct_field)
            content_type_id = getattr(parent, content_type_field.attname)
            content_type = ContentType.objects.get_for_id(content_type_id)
            target_model = apps.get_model(content_type.app_label, content_type.model)

            target_field = parent._meta.get_field(field.fk_field)
            target_meta = target_model._meta

        else:
            raise TypeError("Unsupported type: {}".format(type(field).__name__))

        self._meta = target_meta
        self.pk = getattr(parent, target_field.attname)
        setattr(self, self._meta.pk.name, self.pk)
