from werkzeug.routing import Map, Rule, Submount
from werkzeug.exceptions import HTTPException

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

            action = self.ACTIONS[action_name]
            yield Rule(
                action.path_tpl.format(**(self.__dict__)),
                endpoint=endpoint,
                methods=action.methods
            )


class BaseDispatcher(object):
    request_class = None
    response_class = None

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

        params.update(data=request.deserialized_data)
        params.update(request.args)

        return endpoint(params)

    def __call__(self, environ, start_response):
        request = self.request_class(environ)
        try:
            response = self.response_class(self.dispatch_request(request))
        except HTTPException as e:
            response = self.response_class({'error': e.description}, e.code)
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
