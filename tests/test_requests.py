import pytest

from django.utils.http import urlencode
from rest_framework.test import APITestCase

from tests.models import ExtraModel, SecondModel, ThirdModel


pytestmark = pytest.mark.usefixtures('db')


class RequestTestCase(APITestCase):
    """
    Provides assertion methods for request tests.
    """

    def assertExpanded(self, data):
        """
        Verifies that data is expanded.
        """
        if 'id' not in data:
            raise AssertionError('ID field is missing.')

        if 'content' not in data:
            raise AssertionError('Object is collapsed.')

    def assertCollapsed(self, data):
        """
        Verifies that data is collapsed.
        """
        if 'id' not in data:
            raise AssertionError('ID field is missing.')

        if 'content' in data:
            raise AssertionError('Object is expanded.')


class ListRequestTestCase(RequestTestCase):
    """
    Tests list requests.
    """

    def test_collapsed(self):
        with self.assertNumQueries(1):
            response = self.client.get('/thirds/')

        self.assertTrue(response.data)

        for result in response.data:
            self.assertExpanded(result)
            self.assertCollapsed(result['extra'])
            self.assertCollapsed(result['second'])

    def test_expansion_of_single_item(self):
        with self.assertNumQueries(2):
            response = self.client.get('/thirds/', {
                'expand': 'extra',
            })

        self.assertTrue(response.data)

        for result in response.data:
            self.assertExpanded(result)
            self.assertExpanded(result['extra'])
            self.assertCollapsed(result['second'])

    def test_expansion_of_multiple_items(self):
        with self.assertNumQueries(3):
            response = self.client.get('/thirds/', {
                'expand': 'extra,second',
            })

        self.assertTrue(response.data)

        for result in response.data:
            self.assertExpanded(result)
            self.assertExpanded(result['extra'])
            self.assertExpanded(result['second'])


class DetailRequestTestCaseMixin():
    """
    Mixin for testing requests related to a single object.
    """

    def request(self, expand=None):
        raise NotImplementedError()

    def test_collapsed(self):
        response = self.request()
        result = response.data

        self.assertExpanded(result)
        self.assertCollapsed(result['extra'])
        self.assertCollapsed(result['second'])

    def test_expansion_of_single_item(self):
        response = self.request('extra')
        result = response.data

        self.assertExpanded(result)
        self.assertExpanded(result['extra'])
        self.assertCollapsed(result['second'])

    def test_expansion_of_multiple_items(self):
        response = self.request('extra,second')
        result = response.data

        self.assertExpanded(result)
        self.assertExpanded(result['extra'])
        self.assertExpanded(result['second'])


class RetrieveRequestTestCase(DetailRequestTestCaseMixin, RequestTestCase):
    """
    Tests retrieve requests.
    """

    def request(self, expand=None):
        url = '/thirds/{}/'.format(ThirdModel.objects.first().pk)
        data = {'expand': expand} if expand else {}

        return self.client.get(url, data)


class PatchRequestTestCase(DetailRequestTestCaseMixin, RequestTestCase):
    """
    Tests patch requests.
    """

    def request(self, expand=None):
        query_string = urlencode({'expand': expand} if expand else {})
        url = '/thirds/{}/'.format(ThirdModel.objects.first().pk)

        data = {
            'content': 'update',
        }

        return self.client.patch(url, data, QUERY_STRING=query_string)


class PutRequestTestCase(DetailRequestTestCaseMixin, RequestTestCase):
    """
    Tests put requests.
    """

    def request(self, expand=None):
        query_string = urlencode({'expand': expand} if expand else {})
        url = '/thirds/{}/'.format(ThirdModel.objects.first().pk)

        data = {
            'content': 'update',
            'second': SecondModel.objects.first().pk,
            'extra': ExtraModel.objects.first().pk,
        }

        return self.client.put(url, data, QUERY_STRING=query_string)
