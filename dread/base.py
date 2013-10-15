from werkzeug.routing import Map, Rule, Submount
from werkzeug.exceptions import HTTPException, Unauthorized

from collections import namedtuple


class BaseResource(object):
    Action = namedtuple('Action', ('path_tpl', 'methods'))

    ACTIONS = {
        'list': Action(
            path_tpl='/{name}/',
            methods=['GET']
        ),
        'detail': Action(
            path_tpl='/{name}/<{param_type}:{param_name}>',
            methods=['GET']
        ),
        'create': Action(
            path_tpl='/{name}/',
            methods=['POST']
        ),
        'update': Action(
            path_tpl='/{name}/<{param_type}:{param_name}>',
            methods=['PUT']
        ),
        'delete': Action(
            path_tpl='/{name}/<{param_type}:{param_name}>',
            methods=['DELETE']
        ),
    }

    PROTECTED_ACTIONS = []

    def __init__(self, name=None, param_name=None, param_type=None):
        self.name = name or self.__class__.__name__.lower()
        self.param_name = param_name or ('%s_id' % self.name)
        self.param_type = param_type or 'int'

    def get_rules(self, map):
        for action_name in self.ACTIONS:
            try:
                endpoint = getattr(self, 'on_' + action_name)
            except AttributeError:
                continue

            # In python3 this will work as well:
            # setattr(endpoint, 'requires_auth', \
            #     action_name in self.PROTECTED_ACTIONS)
            endpoint.__dict__['requires_auth'] = \
                (action_name in self.PROTECTED_ACTIONS)

            action = self.ACTIONS[action_name]
            yield Rule(
                action.path_tpl.format(**(self.__dict__)),
                endpoint=endpoint,
                methods=action.methods
            )


class BaseDispatcher(object):
    request_class = None
    response_class = None

    auth_class = None

    def __init__(self):
        self.url_map = Map()

    def add_resource(self, resource, parent_resource=None):
        if parent_resource:
            try:
                for rule in self.url_map.iter_rules(parent_resource.on_detail):
                    detail_rule = rule

                rulefactory = Submount(detail_rule.rule, (resource,))
            except AttributeError:
                raise AttributeError(
                    'The parent resource must define the "on_detail" method')
        else:
            rulefactory = resource

        self.url_map.add(rulefactory)

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        endpoint, params = adapter.match()

        params.update(data=request.data)
        params.update(request.args)

        if endpoint.requires_auth:
            endpoint = self.auth_class(endpoint, request)

        return endpoint(params)

    def __call__(self, environ, start_response):
        request = self.request_class(environ)
        try:
            response = self.response_class(self.dispatch_request(request))
        except HTTPException as e:
            response = self.response_class(
                {'error': e.description},
                e.code,
                headers=e.get_headers())
        return response(environ, start_response)

    def run(self, host='127.0.0.1', port=5000,
            use_debugger=True, use_reloader=True):
        from werkzeug.serving import run_simple
        run_simple(
            host,
            port,
            self,
            use_debugger=use_debugger,
            use_reloader=use_reloader
        )


class BaseAuth(object):
    unauthorized_exception = Unauthorized

    def __init__(self, endpoint, request):
        self.endpoint = endpoint
        self.request = request

    def __call__(self, params):
        if self.authenticate(params):
            return self.endpoint(params)
        else:
            raise self.unauthorized_exception()

    def authenticate(self, params):
        raise NotImplementedError
