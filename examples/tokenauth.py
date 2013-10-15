import sys
sys.path.append('..')

from dread.base import BaseResource
from dread.json import JSONDispatcher
from dread.auth import TokenAuth

from werkzeug.exceptions import NotFound, Unauthorized


class User(BaseResource):
    PROTECTED_ACTIONS = [
        'create', 'update', 'delete'
    ]

    def __init__(self):
        self.users = []
        super(User, self).__init__(name="users", param_name="user_id")

    def on_list(self, params):
        return {'data': self.users}

    def on_detail(self, params):
        try:
            return self.users[params['user_id']]
        except IndexError:
            raise NotFound

    def on_create(self, params):
        new_user = params['data']
        self.users.append(new_user)
        return {'data': new_user}

    def on_update(self, params):
        try:
            self.users[params['user_id']] = params['data']
            return {'data': self.users[params['user_id']]}
        except IndexError:
            raise NotFound

    def on_delete(self, params):
        try:
            del self.users[params['user_id']]
            return {}
        except IndexError:
            raise NotFound


CREDENTIALS = {
    'admin': {
        'password': 'admin',
        'token': 'testtoken'
    }
}


class Session(BaseResource):

    def on_create(self, params):
        user = CREDENTIALS.get(params['data']['username'])
        if user and user['password'] == params['data']['password']:
            return {'token': user['token']}
        raise Unauthorized


class Auth(TokenAuth):

    def check_token(self, token):
        for username, data in CREDENTIALS.iteritems():
            if data['token'] == token:
                return True
        return False


class Dispatcher(JSONDispatcher):
    auth_class = Auth

app = Dispatcher()

app.add_resource(Session())
app.add_resource(User())

if __name__ == '__main__':
    app.run()
