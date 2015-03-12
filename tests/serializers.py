from rest_framework.serializers import HyperlinkedModelSerializer

from rest_framework_expander.serializers import ExpanderSerializerMixin
from tests.models import FirstModel, SecondModel, ThirdModel, ExtraModel


class ExtraSerializer(ExpanderSerializerMixin, HyperlinkedModelSerializer):
    class Meta():
        model = ExtraModel
        fields = ('id', 'url', 'content')


class FirstSerializer(ExpanderSerializerMixin, HyperlinkedModelSerializer):
    extra = ExtraSerializer(read_only=True)

    class Meta():
        model = FirstModel
        fields = ('id', 'url', 'content', 'extra')


class SecondSerializer(ExpanderSerializerMixin, HyperlinkedModelSerializer):
    extra = ExtraSerializer(read_only=True)
    first = FirstSerializer(read_only=True)

    class Meta():
        model = SecondModel
        fields = ('id', 'url', 'content', 'extra', 'first')


class ThirdSerializer(ExpanderSerializerMixin, HyperlinkedModelSerializer):
    extra = ExtraSerializer(read_only=True)
    second = SecondSerializer(read_only=True)

    class Meta():
        model = ThirdModel
        fields = ('id', 'url', 'content', 'extra', 'second')
