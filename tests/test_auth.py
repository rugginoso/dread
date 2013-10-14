import sys
sys.path.append('..')

import unittest
from werkzeug.test import Client
from werkzeug.wrappers import Request, Response

from dread.base import BaseDispatcher, BaseResource, BaseAuth


class TestAuth(BaseAuth):
    def authorize(self, params):
        return params.get('username') == ['admin'] and \
            params.get('password') == ['admin']


class TestDispatcher(BaseDispatcher):
    request_class = Request
    response_class = Response
    auth_class = TestAuth


class TestResource(BaseResource):
    PROTECTED_ACTIONS = (
        'detail',
    )

    def on_list(self, params):
        return {}

    def on_detail(self, params):
        return {}


class TestProtectedAction(unittest.TestCase):
    def setUp(self):
        self.dispatcher = TestDispatcher()
        self.dispatcher.add_resource(TestResource())

        self.client = Client(self.dispatcher, Response)

    def test_protected_action_unauthorized(self):
        resp = self.client.get('/testresource/1')
        self.assertEqual(resp.status_code, 401)

    def test_protected_action_authorized(self):
        resp = self.client.get('/testresource/1?username=admin&password=admin')
        self.assertEqual(resp.status_code, 200)

    def test_unprotected_action(self):
        resp = self.client.get('/testresource/')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
