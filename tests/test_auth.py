import unittest
from base64 import standard_b64encode
from werkzeug.test import Client
from werkzeug.wrappers import Request, Response

from dread.base import BaseDispatcher, BaseResource, BaseAuth
from dread.auth import BasicAuth, TokenAuth


class TestAuth(BaseAuth):

    def authenticate(self, params):
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

    def test_protected_action_wrong_auth(self):
        resp = self.client.get('/testresource/1?username=foo&password=bar')
        self.assertEqual(resp.status_code, 401)

    def test_unprotected_action(self):
        resp = self.client.get('/testresource/')
        self.assertEqual(resp.status_code, 200)


class TestAuth(BasicAuth):

    def check_credientials(self, username, password):
        return username == 'admin' and password == 'admin'


class BasicAuthDispatcher(BaseDispatcher):
    request_class = Request
    response_class = Response
    auth_class = TestAuth


class TestBasicAuth(unittest.TestCase):

    def setUp(self):
        self.dispatcher = BasicAuthDispatcher()
        self.dispatcher.add_resource(TestResource())

        self.client = Client(self.dispatcher, Response)

    def test_protected_action_unauthorized(self):
        resp = self.client.get('/testresource/1')
        self.assertTrue('www-authenticate' in resp.headers)

    def test_protected_action_authorized(self):
        headers = [
            ('Authorization', 'Basic %s' % standard_b64encode('admin:admin'))
        ]

        resp = self.client.get('/testresource/1', headers=headers)
        self.assertEqual(resp.status_code, 200)

    def test_protected_action_wrong_auth(self):
        headers = [
            ('Authorization', 'Basic %s' % standard_b64encode('foo:bar'))
        ]

        resp = self.client.get('/testresource/1', headers=headers)
        self.assertEqual(resp.status_code, 401)


class TestAuth(TokenAuth):

    def check_token(self, token):
        return token == 'testtoken'


class TokenAuthDispatcher(BaseDispatcher):
    request_class = Request
    response_class = Response
    auth_class = TestAuth


class TestTokenAuth(unittest.TestCase):

    def setUp(self):
        self.dispatcher = TokenAuthDispatcher()
        self.dispatcher.add_resource(TestResource())

        self.client = Client(self.dispatcher, Response)

    def test_protected_action_unauthorized(self):
        resp = self.client.get('/testresource/1')
        self.assertTrue('www-authenticate' in resp.headers)

    def test_protected_action_authorized(self):
        headers = [
            ('Authorization', 'Token testtoken')
        ]

        resp = self.client.get('/testresource/1', headers=headers)
        self.assertEqual(resp.status_code, 200)

    def test_protected_action_wrong_auth(self):
        headers = [
            ('Authorization', 'Token foobar')
        ]

        resp = self.client.get('/testresource/1', headers=headers)
        self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main()
