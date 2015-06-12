from django.db.models.fields import FieldDoesNotExist
from django.db.models.loading import get_model

from rest_framework_expander.utils import get_virtual_field


class PKObject(object):
    """
    Mock object for partial instances.

    Provides primary key and model meta.
    """

    def __init__(self, parent, field_name):
        try:
            # Look for a foreign key field.
            field = parent._meta.get_field(field_name)
            self._meta = field.rel.to._meta

        except FieldDoesNotExist:
            # Look for a generic relation virtual field.
            virtual_field = get_virtual_field(parent._meta, field_name)

            # Assume the virtual field is a generic relation.
            content_type_field = parent._meta.get_field(virtual_field.ct_field)
            content_type_id = getattr(parent, content_type_field.attname)

            # Import ContentType only if necessary.
            from django.contrib.contenttypes.models import ContentType

            # Find the target model for the generic relation.
            content_type = ContentType.objects.get_for_id(content_type_id)
            model = get_model(content_type.app_label, content_type.model)

            # We now know where the primary key is and which model it points to.
            field = parent._meta.get_field(virtual_field.fk_field)
            self._meta = model._meta

        # Set the attributes for the primary key.
        self.pk = getattr(parent, field.attname)
        setattr(self, self._meta.pk.name, self.pk)
