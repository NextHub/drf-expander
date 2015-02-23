from rest_framework.serializers import ModelSerializer

from rest_framework_expander.serializers import ExpanderSerializerMixin
from tests.models import FirstModel, SecondModel, ThirdModel, ExtraModel


class ExtraSerializer(ExpanderSerializerMixin, ModelSerializer):
    class Meta():
        model = ExtraModel


class FirstSerializer(ExpanderSerializerMixin, ModelSerializer):
    extra = ExtraSerializer()

    class Meta():
        model = FirstModel


class SecondSerializer(ExpanderSerializerMixin, ModelSerializer):
    first = FirstSerializer()
    extra = ExtraSerializer()

    class Meta():
        model = SecondModel


class ThirdSerializer(ExpanderSerializerMixin, ModelSerializer):
    second = SecondSerializer()
    extra = ExtraSerializer()

    class Meta():
        model = ThirdModel
