from django.utils import six
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory

from rest_framework_expander.adapters import ExpanderAdapter
from rest_framework_expander.exceptions import ExpanderDepthBreached, ExpanderFieldMissing
from rest_framework_expander.parsers import ExpanderParser
from tests.serializers import ThirdSerializer


class ExpansionParserTestCase(APITestCase):
    """
    Tests parsing of plain expansion.
    """

    def parse_expand(self, expand=None, settings=dict()):
        """
        Helper method for running the parser.
        """
        params = dict()

        if expand is not None:
            params['expand'] = expand

        request = Request(APIRequestFactory().get('/thirds/', params))
        serializer = ThirdSerializer(context={'request': request})
        adapter = ExpanderAdapter(serializer)
        parser = ExpanderParser(adapter)

        for key, value in six.iteritems(settings):
            setattr(parser, key, value)

        return parser.parse()

    def child_count(self, expander, *args):
        """
        Helper method for counting expander children.
        """
        for arg in args:
            expander = expander.children[arg]

        return len(expander.children)

    def test_without_query_parameter(self):
        expander = self.parse_expand()

        self.assertEqual(0, self.child_count(expander))

    def test_empty_query_parameter(self):
        expander = self.parse_expand('')

        self.assertEqual(0, self.child_count(expander))

    def test_single_item(self):
        expander = self.parse_expand('second')

        self.assertEqual(1, self.child_count(expander))
        self.assertEqual(0, self.child_count(expander, 'second'))

    def test_multiple_items(self):
        expander = self.parse_expand('extra,second')

        self.assertEqual(2, self.child_count(expander))
        self.assertEqual(0, self.child_count(expander, 'extra'))
        self.assertEqual(0, self.child_count(expander, 'second'))

    def test_ignored_depth_breach(self):
        expander = self.parse_expand('second.first', {
            'fail_on_depth_breached': False,
            'max_depth': 1,
        })

        self.assertEqual(1, self.child_count(expander))
        self.assertEqual(0, self.child_count(expander, 'second'))

    def test_failed_depth_breach(self):
        self.assertRaises(ExpanderDepthBreached, self.parse_expand, 'second.first', {
            'fail_on_depth_breached': True,
            'max_depth': 1,
        })

    def test_multiple_levels(self):
        expander = self.parse_expand('second.first', {
            'max_depth': 2,
        })

        self.assertEqual(1, self.child_count(expander))
        self.assertEqual(1, self.child_count(expander, 'second'))
        self.assertEqual(0, self.child_count(expander, 'second', 'first'))

    def test_multiple_levels_and_items(self):
        expander = self.parse_expand('extra,second.first,second.extra', {
            'max_depth': 2,
        })

        self.assertEqual(2, self.child_count(expander))
        self.assertEqual(0, self.child_count(expander, 'extra'))
        self.assertEqual(2, self.child_count(expander, 'second'))
        self.assertEqual(0, self.child_count(expander, 'second', 'first'))
        self.assertEqual(0, self.child_count(expander, 'second', 'extra'))

    def test_ignored_field_missing(self):
        expander = self.parse_expand('alpaca', {
            'fail_on_field_missing': False,
        })

        self.assertEqual(0, self.child_count(expander))

    def test_failed_field_missing(self):
        self.assertRaises(ExpanderFieldMissing, self.parse_expand, 'alpaca', {
            'fail_on_field_missing': True,
        })

    def test_custom_separators(self):
        expander = self.parse_expand('extra+second::first', {
            'expansion_item_separator': '+',
            'expansion_path_separator': '::',
            'max_depth': 2,
        })

        self.assertEqual(2, self.child_count(expander))
        self.assertEqual(0, self.child_count(expander, 'extra'))
        self.assertEqual(1, self.child_count(expander, 'second'))
        self.assertEqual(0, self.child_count(expander, 'second', 'first'))

    def test_custom_query_parameter(self):
        request = Request(APIRequestFactory().get('/thirds/', {'pony': 'extra'}))
        serializer = ThirdSerializer(context={'request': request})
        adapter = ExpanderAdapter(serializer)
        parser = ExpanderParser(adapter)
        parser.expansion_key = 'pony'

        expander = parser.parse()
        self.assertEqual(1, self.child_count(expander))
        self.assertEqual(0, self.child_count(expander, 'extra'))
