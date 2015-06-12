from collections import OrderedDict
from django.db.models.fields import FieldDoesNotExist
from django.utils import six
from rest_framework.fields import SkipField
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer
from rest_framework.settings import import_from_string

from rest_framework_expander.context import ExpanderContext
from rest_framework_expander.relations import PKObject
from rest_framework_expander.settings import expander_settings


class ExpanderSerializerMixin(object):
    """
    Provides both collapsed and expanded representations.
    """

    def __init__(self, *args, **kwargs):
        expanded = kwargs.pop('expanded', None)

        if expanded is not None:
            self._expanded = expanded

        super(ExpanderSerializerMixin, self).__init__(*args, **kwargs)

    @property
    def expander(self):
        """
        The expander context for this serializer, or None.
        """
        if not hasattr(self, '_expander'):
            if 'expander' in self.context:
                root = self.context['expander']
                self._expander = root.get_child_by_serializer(self)
            elif expander_settings.DEFAULT_EXPANDED:
                root = ExpanderContext(None, None)
                self.context['expander'] = root
                self._expander = root.get_child_by_serializer(self)
            else:
                self._expander = None

        return self._expander

    @property
    def expanded(self):
        """
        True if this serializer should be expanded.
        """
        if not hasattr(self, '_expanded'):
            self._expanded = self.expander is not None

        return self._expanded

    @property
    def collapsed_fields(self):
        """
        Dictionary containing the fields of the collapsed representation.
        """
        if not hasattr(self, '_collapsed_fields'):
            meta = getattr(self, 'Meta', None)
            field_names = getattr(meta, 'collapsed_fields', expander_settings.COLLAPSED_FIELDS)
            self._collapsed_fields = OrderedDict()

            for field_name in field_names:
                if field_name in self.fields.keys():
                    self._collapsed_fields[field_name] = self.fields[field_name]

        return self._collapsed_fields

    def get_attribute(self, instance):
        if self.expanded:
            return self.get_expanded_attribute(instance)
        else:
            return self.get_collapsed_attribute(instance)

    def get_expanded_attribute(self, instance):
        """
        Returns attribute for the expanded representation.
        """
        return super(ExpanderSerializerMixin, self).get_attribute(instance)

    def get_collapsed_attribute(self, instance):
        """
        Returns attribute for the collapsed representation.
        """
        try:
            obj = PKObject(instance, self.field_name)
            return obj if obj.pk is not None else None
        except (FieldDoesNotExist, AttributeError):
            return super(ExpanderSerializerMixin, self).get_attribute(instance)

    def to_representation(self, instance):
        if self.expanded:
            return self.to_expanded_representation(instance)
        else:
            return self.to_collapsed_representation(instance)

    def to_expanded_representation(self, instance):
        """
        Returns the expanded representation.
        """
        return super(ExpanderSerializerMixin, self).to_representation(instance)

    def to_collapsed_representation(self, instance):
        """
        Returns the collapsed representation.
        """
        ret = OrderedDict()
        fields = [field for field in self.collapsed_fields.values() if not field.write_only]

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret


class ExpanderListSerializer(ExpanderSerializerMixin, Serializer):
    """
    Serializer for nested list expansion.
    """

    def __init__(self, child_class, view_name, *args, **kwargs):
        self.view_name = view_name

        kwargs['read_only'] = True
        kwargs['source'] = '*'
        self._child_specification = (child_class, args, kwargs)

        super(ExpanderListSerializer, self).__init__(read_only=True)

    @property
    def child(self):
        if not hasattr(self, '_child'):
            child_class, args, kwargs = self._child_specification

            if six.text_type(child_class):
                child_class = import_from_string(child_class, None)

            self._child = child_class(*args, **kwargs)

        return self._child

    def bind(self, field_name, parent):
        super(ExpanderListSerializer, self).bind(field_name, parent)
        self.child.bind('results', self)

    @property
    def expander(self):
        return self.child.expander

    @property
    def expanded(self):
        return self.child.expanded

    def get_expanded_attribute(self, instance):
        return instance

    def get_collapsed_attribute(self, instance):
        return instance

    def to_expanded_representation(self, instance):
        try:
            objects = self.expander.data[instance.pk]
        except (AttributeError, KeyError):
            objects = getattr(instance, self.source).all()[:3]

        return OrderedDict((
            ('url', reverse(self.view_name, (instance.pk,), request=self.context['request'])),
            ('results', [self.child.to_representation(obj) for obj in objects]),
        ))

    def to_collapsed_representation(self, instance):
        return OrderedDict((
            ('url', reverse(self.view_name, (instance.pk,), request=self.context['request'])),
        ))


class ExpanderProxySerializer(Serializer):
    """
    Serializer with lazy imports for resolving cycles.
    """

    def __init__(self, child_class, *args, **kwargs):
        self._child_specification = (child_class, args, kwargs)
        super(ExpanderProxySerializer, self).__init__(read_only=True)

    @property
    def child(self):
        if not hasattr(self, '_child'):
            child_class, args, kwargs = self._child_specification

            if six.text_type(child_class):
                child_class = import_from_string(child_class, None)

            self._child = child_class(*args, **kwargs)

        return self._child

    def bind(self, field_name, parent):
        super(ExpanderProxySerializer, self).bind(field_name, parent)
        self.child.bind(field_name, parent)

    @property
    def expander(self):
        return self.child.expander

    @property
    def expanded(self):
        return self.child.expanded

    def get_attribute(self, instance):
        return self.child.get_attribute(instance)

    def to_representation(self, instance):
        return self.child.to_representation(instance)
