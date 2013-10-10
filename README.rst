     &&&&&
    & @ @ &   0
    &  |  &  0
    & \_o===0
    &\ _ /&
    &     &
    &     &     DREAD - REST microframework

Overview
========
*The code is in an alpha stage*

DREAD is a web microframework based on [Werkzeug](https://github.com/mitsuhiko/werkzeug) explicitely wrote to implement REST services.
It support high level resource action definition and nested resources.

Example
=======
```python
from dread.base import BaseResource
from dread.json import JSONDispatcher

from werkzeug.exceptions import NotFound


class User(BaseResource):
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

class Item(BaseResource):
    def __init__(self):
        super(Item, self).__init__(name='items', param_name='item_id')

    def on_list(self, params):
        return {'owner': params['user_id']}

    def on_detail(self, params):
        return {'owner': params['user_id'], 'item': params['item_id']}


app = JSONDispatcher()

users_resource = User()
app.add_resource(users_resource)
app.add_resource(Item(), users_resource)

if __name__ == '__main__':
    app.run()
```