from rest_framework.viewsets import ModelViewSet

from rest_framework_expander.views import ExpanderListModelMixin
from tests.models import ExtraModel, FirstModel, SecondModel, ThirdModel
from tests.serializers import ExtraSerializer, FirstSerializer, SecondSerializer, ThirdSerializer


class ExtraViewSet(ExpanderListModelMixin, ModelViewSet):
    queryset = ExtraModel.objects.all()
    serializer_class = ExtraSerializer


class FirstViewSet(ExpanderListModelMixin, ModelViewSet):
    queryset = FirstModel.objects.all()
    serializer_class = FirstSerializer


class SecondViewSet(ExpanderListModelMixin, ModelViewSet):
    queryset = SecondModel.objects.all()
    serializer_class = SecondSerializer


class ThirdViewSet(ExpanderListModelMixin, ModelViewSet):
    queryset = ThirdModel.objects.all()
    serializer_class = ThirdSerializer
