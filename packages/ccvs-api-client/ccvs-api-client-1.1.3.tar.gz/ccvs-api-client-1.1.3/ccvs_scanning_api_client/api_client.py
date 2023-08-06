# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import json
import logging
import re

from requests import request

import ccvs_scanning_api_client.models
from ccvs_scanning_api_client import exceptions

LOGGER = logging.getLogger(__name__)


class ApiClient(object):

    ERRORS = {
        400: exceptions.ValidationError,
        401: exceptions.Unauthorized,
        403: exceptions.Forbidden,
        404: exceptions.NotFound,
        'default': exceptions.ApiError,
    }

    def __init__(self, config):
        self.config = config

    def make_request(
            self, method, path, params=None,
            data=None, response_type=None):

        path = path if path[-1] == '/' else path + '/'
        request_url = f'{self.config.host}{path}'

        headers = {
            'Content-Type': 'application/json'
        }

        if data:
            data = json.dumps(self.serialize(data))

        try:
            response = request(
                method,
                request_url,
                params=params,
                data=data,
                headers=headers
            )
        except Exception as error:
            LOGGER.error(error)
            raise exceptions.ApiError(0, 'Error in request')
        else:
            response_body = self._parser_response(response)
            return self.deserialize(response_body, response_type)

    def _parser_response(self, response):

        status_code = response.status_code
        try:
            content = response.json()
        except json.JSONDecodeError:
            content = response.content

        if response.ok:
            return content
        elif self.ERRORS.get(status_code):
            error_class = self.ERRORS.get(status_code)
            raise error_class(status_code, content)
        else:
            error_class = self.ERRORS.get('default')
            raise error_class(status_code, content)

    def deserialize(self, response, response_type):
        """
        Deserialize(s response into an object.

        :param response: RESTResponse object to be deserialized.
        :param response_type: string of class name.

        :return: deserialized object.
        """

        if type(response_type) == str:
            if response_type.startswith('list['):
                sub_kls = re.match(r'list\[(.*)\]', response_type).group(1)
                return [self.deserialize(sub_data, sub_kls)
                        for sub_data in response]

            if response_type.startswith('dict'):
                return response

            response_type = getattr(
                ccvs_scanning_api_client.models, response_type)
            return self.deserialize(response, response_type)
        else:
            return response_type(**response)

    def serialize(self, data):
        data = data.to_dict()
        return data
