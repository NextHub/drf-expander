from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.test import APITestCase, APIRequestFactory

from rest_framework_expander.adapters import get_serializer_adapter, SerializerAdapter, ListSerializerAdapter
from rest_framework_expander.exceptions import ExpanderAdapterMissing
from tests.serializers import ThirdSerializer


class AdapterTestCaseMixin():
    """
    Mixin containing generic adapter test cases.
    """

    def test_get_serializer_adapter(self):
        adapter = get_serializer_adapter(self.serializer)
        self.assertIsInstance(adapter, self.adapter_class)

    def test_context(self):
        self.assertIs(self.context, self.adapter.context)

    def test_fields(self):
        self.assertIs(self.fields, self.adapter.fields)

    def test_instance(self):
        dummy = object()

        self.assertIs(self.instance, self.adapter.instance)
        self.assertIsNot(dummy, self.adapter.instance)

        self.adapter.instance = dummy

        self.assertIsNot(self.instance, self.adapter.instance)
        self.assertIs(dummy, self.adapter.instance)

    def test_serializer(self):
        self.assertIs(self.serializer, self.adapter.serializer)

    def test_object_serializer(self):
        self.assertIs(self.object_serializer, self.adapter.object_serializer)

    def test_many(self):
        self.assertIs(self.many, self.adapter.many)


class SerializerAdapterTestCase(AdapterTestCaseMixin, APITestCase):
    """
    Tests SerializerAdapter.
    """

    def setUp(self):
        self.request = Request(APIRequestFactory().get('/thirds/0/'))
        self.context = {'request': self.request}
        self.instance = object()

        self.many = False
        self.serializer = ThirdSerializer(instance=self.instance, context=self.context, many=self.many)

        self.object_serializer = self.serializer
        self.fields = self.object_serializer.fields

        self.adapter_class = SerializerAdapter
        self.adapter = self.adapter_class(self.serializer)


class ListSerializerAdapterTestCase(AdapterTestCaseMixin, APITestCase):
    """
    Tests ListSerializerAdapter.
    """

    def setUp(self):
        self.request = Request(APIRequestFactory().get('/thirds/'))
        self.context = {'request': self.request}
        self.instance = object()

        self.many = True
        self.serializer = ThirdSerializer(instance=self.instance, context=self.context, many=self.many)

        self.object_serializer = self.serializer.child
        self.fields = self.object_serializer.fields

        self.adapter_class = ListSerializerAdapter
        self.adapter = self.adapter_class(self.serializer)


class MiscellaneousAdapterTestCase(APITestCase):
    """
    Tests functionality not directly related to an adapter class.
    """

    def test_expander_adapter_missing(self):
        self.assertRaises(ExpanderAdapterMissing, get_serializer_adapter, BaseSerializer())
