from rest_framework.viewsets import ViewSet

from rest_framework_expander.views import ExpanderViewMixin
from tests.models import ExtraModel, FirstModel, SecondModel, ThirdModel
from tests.serializers import ExtraSerializer, FirstSerializer, SecondSerializer, ThirdSerializer


class ExtraViewSet(ExpanderViewMixin, ViewSet):
    queryset = ExtraModel.objects.all()
    serializer_class = ExtraSerializer


class FirstViewSet(ExpanderViewMixin, ViewSet):
    queryset = FirstModel.objects.all()
    serializer_class = FirstSerializer


class SecondViewSet(ExpanderViewMixin, ViewSet):
    queryset = SecondModel.objects.all()
    serializer_class = SecondSerializer


class ThirdViewSet(ExpanderViewMixin, ViewSet):
    queryset = ThirdModel.objects.all()
    serializer_class = ThirdSerializer
