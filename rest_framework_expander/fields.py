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

        return instance


class CollapsedHyperlinkField(ReadOnlyField):
    """
    Returns the instance URL without making a database query.
    """

    def get_attribute(self, instance):
        if self.field_name not in self.parent.fields:
            raise SkipField()

        try:
            viewname = self.parent.fields[self.field_name].view_name
            args = (instance,)
            request = self.context['request']

            return reverse(viewname, args, request=request)

        except (AttributeError, KeyError, NoReverseMatch):
            raise SkipField()
