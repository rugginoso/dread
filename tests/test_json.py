import unittest
from werkzeug.test import EnvironBuilder
from werkzeug.exceptions import BadRequest

from dread.json import JSONRequest, JSONResponse


class TestRequest(unittest.TestCase):
    def test_mimetype_fail(self):
        builder = EnvironBuilder(method='POST', data='{"foo": "bar"}')
        request = JSONRequest(builder.get_environ())

        with self.assertRaises(BadRequest):
            request.data

    def test_mimetype_success(self):
        builder = EnvironBuilder(method='POST', data='{"foo": "bar"}')
        builder.content_type = 'application/json'
        request = JSONRequest(builder.get_environ())

        self.assertEqual(request.data, {'foo': 'bar'})


class TestResponse(unittest.TestCase):
    def test_mimetype(self):
        response = JSONResponse({})

        self.assertEqual(response.mimetype, 'application/json')


if __name__ == '__main__':
    unittest.main()
