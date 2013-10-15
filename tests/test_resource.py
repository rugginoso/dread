import unittest

from dread.base import BaseResource


class TestRuleGeneration(unittest.TestCase):

    def setUp(self):
        def endpoint(self, params):
            pass

        self.resource = BaseResource()
        self.endpoint = endpoint

    def test_list(self):
        self.resource.on_list = self.endpoint

        rules = list(self.resource.get_rules(None))

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/baseresource/')
        self.assertEqual(rules[0].endpoint, self.endpoint)
        self.assertEqual(rules[0].methods, {'GET', 'HEAD'})

    def test_create(self):
        self.resource.on_create = self.endpoint

        rules = list(self.resource.get_rules(None))

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/baseresource/')
        self.assertEqual(rules[0].endpoint, self.endpoint)
        self.assertEqual(rules[0].methods, {'POST'})

    def test_detail(self):
        self.resource.on_detail = self.endpoint

        rules = list(self.resource.get_rules(None))

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/baseresource/<int:baseresource_id>')
        self.assertEqual(rules[0].endpoint, self.endpoint)
        self.assertEqual(rules[0].methods, {'GET', 'HEAD'})

    def test_update(self):
        self.resource.on_update = self.endpoint

        rules = list(self.resource.get_rules(None))

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/baseresource/<int:baseresource_id>')
        self.assertEqual(rules[0].endpoint, self.endpoint)
        self.assertEqual(rules[0].methods, {'PUT'})

    def test_delete(self):
        self.resource.on_delete = self.endpoint

        rules = list(self.resource.get_rules(None))

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/baseresource/<int:baseresource_id>')
        self.assertEqual(rules[0].endpoint, self.endpoint)
        self.assertEqual(rules[0].methods, {'DELETE'})


if __name__ == '__main__':
    unittest.main()
