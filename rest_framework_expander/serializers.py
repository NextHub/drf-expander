from rest_framework_expander.settings import expander_settings


class ExpanderSerializerMixin():
    """
    Provides both collapsed and expanded representations.
    """

    @property
    def expander(self):
        """
        The expander context for this serializer, or None.
        """
        if not hasattr(self, '_expander'):
            if 'expander' in self.context:
                root = self.context['expander']
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
            if 'expander' in self.context:
                self._expanded = self.expander is not None
            else:
                self._expanded = expander_settings.DEFAULT_EXPANDED

        return self._expanded

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
        return instance

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
        return dict()
