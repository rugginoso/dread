from werkzeug.exceptions import Unauthorized
from base64 import standard_b64decode

from .base import BaseAuth


class BasicAuth(BaseAuth):

    class Unauthorized(Unauthorized):

        def __init__(self, *args, **kwargs):
            self.realm = kwargs.get('realm') or 'Authorization required'
            super(Unauthorized, self).__init__(*args, **kwargs)

        def get_headers(self, enviroment=None):
            headers = super(Unauthorized, self).get_headers()
            headers.append(
                ('WWW-Authenticate', 'Basic realm="%s"' % self.realm)
            )
            return headers
    unauthorized_exception = Unauthorized

    def authenticate(self, params):
        auth_header = self.request.headers.get('authorization')
        if auth_header:
            method, user_pass = auth_header.split()
            if method.lower() == 'basic':
                try:
                    username, password = standard_b64decode(
                        user_pass).split(':')
                    return self.check_credientials(username, password)
                except ValueError:
                    return False
        return False

    def check_credientials(self, username, password):
        raise NotImplementedError
