from __future__ import absolute_import

from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import BadRequest
from werkzeug.utils import cached_property

import json

from .base import BaseDispatcher


class JSONRequest(Request):

    @cached_property
    def data(self):
        data = super(JSONRequest, self).data
        if data:
            if 'json' not in self.environ.get('CONTENT_TYPE', ''):
                raise BadRequest('Not a JSON request')
            try:
                return json.loads(data)
            except Exception:
                raise BadRequest('Unable to read JSON request')


class JSONResponse(Response):

    def __init__(self, response, *args, **kwargs):
        response = json.dumps(response)
        kwargs['mimetype'] = 'application/json'
        super(JSONResponse, self).__init__(response, *args, **kwargs)


class JSONDispatcher(BaseDispatcher):

    request_class = JSONRequest
    response_class = JSONResponse
