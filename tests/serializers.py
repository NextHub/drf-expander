from rest_framework.serializers import ModelSerializer

from rest_framework_expander.serializers import ExpanderSerializerMixin
from tests.models import FirstModel, SecondModel, ThirdModel, ExtraModel


class ExtraSerializer(ExpanderSerializerMixin, ModelSerializer):
    class Meta():
        model = ExtraModel


class FirstSerializer(ExpanderSerializerMixin, ModelSerializer):
    extra = ExtraSerializer(read_only=True)

    class Meta():
        model = FirstModel


class SecondSerializer(ExpanderSerializerMixin, ModelSerializer):
    first = FirstSerializer(read_only=True)
    extra = ExtraSerializer(read_only=True)

    class Meta():
        model = SecondModel


class ThirdSerializer(ExpanderSerializerMixin, ModelSerializer):
    second = SecondSerializer(read_only=True)
    extra = ExtraSerializer(read_only=True)

    class Meta():
        model = ThirdModel
