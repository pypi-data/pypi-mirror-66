# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import six


class Vendor(object):

    swagger_types = {
        'id': 'str',
        'name': 'str',
        'credentials': 'dict'
    }

    def __init__(self, id=None, name=None, credentials=None):

        self._id = None
        self._name = None

        self._credentials = None

        if id is not None:
            self.id = id
        self.name = name
        self.credentials = credentials

    @property
    def id(self):
        """
        Gets the id of this Vendor.

        :return: The id of this Vendor.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Vendor.

        :param id: The id of this Vendor.
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Vendor.

        :return: The name of this Vendor.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Vendor.

        :param name: The name of this Vendor.
        :type: str
        """
        if name is None:
            raise ValueError('Invalid value for `name`, must not be `None`')
        if name is not None and len(name) > 100:
            raise ValueError(
                'Invalid value for `name`, length must be less than or '
                'equal to `100`')
        if name is not None and len(name) < 1:
            raise ValueError(
                'Invalid value for `name`, length must be greater than or '
                'equal to `1`')

        self._name = name

    @property
    def credentials(self):
        """
        Gets the credentials of this Vendor.

        :return: The credentials of this Vendor.
        :rtype: str
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this Vendor.

        :param credentials: The credentials of this Vendor.
        :type: str
        """
        if credentials is None:
            raise ValueError(
                'Invalid value for `credentials`, must not be `None`')

        self._credentials = credentials

    def to_dict(self):
        """Returns the model properties as a dict."""

        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, 'to_dict') else x,
                    value
                ))
            elif hasattr(value, 'to_dict'):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], 'to_dict') else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Vendor, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def __eq__(self, other):
        """Returns true if both objects are equal."""
        if not isinstance(other, Vendor):
            return False

        return self.__dict__ == other.__dict__

    @property
    def __dict__(self):
        """Returns a custom dict."""

        return self.to_dict()
