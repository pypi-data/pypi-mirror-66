# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class ApiException(Exception):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.getheaders()
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self):
        """Custom error messages for exception."""
        error_message = '({0})\n'\
                        'Reason: {1}\n'.format(self.status, self.reason)
        if self.headers:
            error_message += 'HTTP response headers: {0}\n'.format(
                self.headers)

        if self.body:
            error_message += 'HTTP response body: {0}\n'.format(self.body)

        return error_message


class ApiError(ApiException):
    def __init__(self, status=None, reason=None, http_resp=None):
        super(ApiError, self).__init__(status, reason, http_resp)


class ValidationError(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(ValidationError, self).__init__(status, reason, http_resp)


class Unauthorized(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(Unauthorized, self).__init__(status, reason, http_resp)


class Forbidden(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(Forbidden, self).__init__(status, reason, http_resp)


class NotFound(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(NotFound, self).__init__(status, reason, http_resp)
