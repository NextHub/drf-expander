from django.core.urlresolvers import NoReverseMatch
from rest_framework.fields import ReadOnlyField, SkipField
from rest_framework.reverse import reverse


class CollapsedIdentityField(ReadOnlyField):
    """
    Returns the instance ID without making a database query.
    """

    def get_attribute(self, instance):
        if self.field_name not in self.parent.fields:
            raise SkipField()

        source = self.parent.source + '_id'

        if hasattr(instance, source):
            return getattr(instance, source)
        else:
            raise SkipField()


class CollapsedHyperlinkField(CollapsedIdentityField):
    """
    Returns the instance URL without making a database query.
    """

    def get_attribute(self, instance):
        identity = super(CollapsedHyperlinkField, self).get_attribute(instance)

        try:
            viewname = self.parent.fields[self.field_name].view_name
            args = (identity,)
            request = self.context['request']

            return reverse(viewname, args, request=request)

        except (AttributeError, KeyError, NoReverseMatch):
            raise SkipField()
