import unittest

from werkzeug.test import Client
from werkzeug.wrappers import Request, Response

from dread.base import BaseDispatcher, BaseResource


class TestRuleGeneration(unittest.TestCase):

    def setUp(self):
        self.dispatcher = BaseDispatcher()

    def test_add_resource(self):
        def endpoint(self, params):
            pass

        resource = BaseResource(name='resource')
        resource.on_list = endpoint

        self.dispatcher.add_resource(resource)

        rules = list(self.dispatcher.url_map.iter_rules())

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].endpoint, endpoint)

    def test_add_nested_resource(self):
        def endpoint(self, params):
            pass

        def nested_endpoint(self, params):
            pass

        resource = BaseResource(name='resource')
        resource.on_detail = endpoint

        nested_resource = BaseResource(name='nested_resource')
        nested_resource.on_detail = nested_endpoint

        self.dispatcher.add_resource(resource)
        self.dispatcher.add_resource(nested_resource, resource)

        rules = list(self.dispatcher.url_map.iter_rules(nested_endpoint))

        self.assertEqual(len(rules), 1)
        self.assertEqual(
            rules[0].rule,
            '/resource/<int:resource_id>/nested_resource/<int:nested_resource_id>')

    def test_add_nested_resource_without_details(self):
        def endpoint(self, params):
            pass

        def nested_endpoint(self, params):
            pass

        resource = BaseResource(name='resource')
        resource.on_list = endpoint

        nested_resource = BaseResource(name='nested_resource')
        nested_resource.on_detail = nested_endpoint

        self.dispatcher.add_resource(resource)

        with self.assertRaises(AttributeError):
            self.dispatcher.add_resource(nested_resource, resource)


class TestDispatcher(BaseDispatcher):
    request_class = Request
    response_class = Response


class TestResource(BaseResource):

    def __init__(self, testcase, *args, **kwargs):
        self.testcase = testcase
        super(TestResource, self).__init__(*args, **kwargs)

    def on_list(self, params):
        return self._endpoint(params)

    def on_detail(self, params):
        return self._endpoint(params)

    def on_create(self, params):
        return self._endpoint(params)

    def on_update(self, params):
        return self._endpoint(params)

    def on_delete(self, params):
        return self._endpoint(params)

    def _endpoint(self, params):
        self.testcase.params = params
        return {}


class TestParams(unittest.TestCase):

    def setUp(self):
        self.dispatcher = TestDispatcher()

        resource = TestResource(self, name='resource')
        nested_resource = TestResource(self, name='nested_resource')

        self.dispatcher.add_resource(resource)
        self.dispatcher.add_resource(nested_resource, resource)

        self.client = Client(self.dispatcher, Response)

        self.params = None

    def test_url_params(self):
        self.client.get('/resource/1/nested_resource/2')

        self.assertTrue('resource_id' in self.params)
        self.assertEqual(self.params['resource_id'], 1)

        self.assertTrue('nested_resource_id' in self.params)
        self.assertEqual(self.params['nested_resource_id'], 2)

    def test_query_string(self):
        self.client.get('/resource/1/nested_resource/2?key=value')

        self.assertTrue('key' in self.params)
        self.assertEqual(self.params['key'], ['value'])

    def test_create_data(self):
        self.client.post('/resource/', data='test data')

        self.assertTrue('data' in self.params)
        self.assertEqual(self.params['data'], 'test data')

    def test_update_data(self):
        self.client.put('/resource/1', data='test data')

        self.assertTrue('data' in self.params)
        self.assertEqual(self.params['data'], 'test data')


if __name__ == '__main__':
    unittest.main()
