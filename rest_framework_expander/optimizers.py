from collections import OrderedDict
from copy import deepcopy
from django.utils import six
from rest_framework.utils.serializer_helpers import BindingDict

from rest_framework_expander import utils
from rest_framework_expander.exceptions import ExpanderContextMissing


class ExpanderOptimizer(object):
    """
    Provides a minimal class for implementing optimizations.
    """
    _creation_counter = 0

    def __init__(self, adapter=None):
        self._creation_counter = ExpanderOptimizer._creation_counter
        ExpanderOptimizer._creation_counter += 1

        self.parent = None
        self.adapter = adapter

    def bind(self, parent, field_name):
        self.parent = parent
        self.field_name = field_name
        self.adapter = parent.adapter

    @property
    def expander(self):
        if not hasattr(self, '_expander'):
            if self.parent:
                self._expander = self.parent.expander.children[self.field_name]
            elif self.adapter:
                self._expander = self.adapter.context['expander']
            else:
                raise ExpanderContextMissing()

        return self._expander

    def to_optimized_queryset(self, queryset):
        """
        Performs optimizations before the queryset has been evaluated.
        """

        return queryset

    def to_optimized_objects(self, objects):
        """
        Performs optimizations after the queryset has been evaluated.
        """

        return objects


class ExpanderOptimizerSetMeta(type):
    """
    Handles field declarations for ExpanderOptimizerSet.

    Based on Django REST Framework's SerializerMetaclass.
    """

    @classmethod
    def _get_declared_optimizers(cls, bases, attrs):
        optimizers = [
            (optimizer_name, attrs.pop(optimizer_name))
            for optimizer_name, obj in list(attrs.items())
            if isinstance(obj, ExpanderOptimizer)
        ]

        optimizers.sort(key=lambda x: x[1]._creation_counter)

        for base in reversed(bases):
            if hasattr(base, '_declared_optimizers'):
                optimizers = list(base._declared_optimizers.items()) + optimizers

        return OrderedDict(optimizers)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_optimizers'] = cls._get_declared_optimizers(bases, attrs)
        return super(ExpanderOptimizerSetMeta, cls).__new__(cls, name, bases, attrs)


@six.add_metaclass(ExpanderOptimizerSetMeta)
class ExpanderOptimizerSet(ExpanderOptimizer):
    """
    Provides a minimal class for combining several optimizers.
    """

    def get_optimizers(self):
        return deepcopy(self._declared_optimizers)

    @property
    def optimizers(self):
        if not hasattr(self, '_optimizers'):
            self._optimizers = BindingDict(self)
            for key, value in six.iteritems(self.get_optimizers()):
                self._optimizers[key] = value

        return self._optimizers

    def to_optimized_queryset(self, queryset):
        for name, optimizer in six.iteritems(self.optimizers):
            if name in self.expander.children:
                queryset = optimizer.to_optimized_queryset(queryset)

        return queryset

    def to_optimized_objects(self, objects):
        for name, optimizer in six.iteritems(self.optimizers):
            if name in self.expander.children:
                objects = optimizer.to_optimized_objects(objects)

        return objects


class PrefetchExpanderOptimizerSet(ExpanderOptimizerSet):
    """
    ExpanderOptimizerSet which defaults to calling prefetch related.
    """

    def get_optimizers(self):
        optimizers = deepcopy(self._declared_optimizers)

        for name in self.expander.children.keys():
            if name not in optimizers:
                optimizers[name] = PrefetchExpanderOptimizerSet()

        return optimizers

    def to_optimized_queryset(self, queryset):
        if hasattr(queryset, 'model'):
            source_path = utils.get_serializer_source_path(self.expander.serializer)
            source_name = utils.get_model_source_name(source_path, queryset.model)

            if source_name:
                queryset = queryset.prefetch_related(source_name)

        return super(PrefetchExpanderOptimizerSet, self).to_optimized_queryset(queryset)


class SelectExpanderOptimizerSet(ExpanderOptimizerSet):
    """
    ExpanderOptimizerSet which defaults to calling select related.
    """

    def get_optimizers(self):
        optimizers = deepcopy(self._declared_optimizers)

        for name in self.expander.children.keys():
            if name not in optimizers:
                optimizers[name] = SelectExpanderOptimizerSet()

        return optimizers

    def to_optimized_queryset(self, queryset):
        if hasattr(queryset, 'model'):
            source_path = utils.get_serializer_source_path(self.expander.serializer)
            source_name = utils.get_model_source_name(source_path, queryset.model)

            if source_name:
                queryset = queryset.select_related(source_name)

        return super(SelectExpanderOptimizerSet, self).to_optimized_queryset(queryset)
