# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class VendorsApi(object):

    def __init__(self, api_client):
        self.api_client = api_client

    def vendors_create(self, data, **kwargs):
        """
        vendors_create.

        :param Vendor data: (required)
        :return: Vendor
        """

        path = f'container-scanning/vendors/'

        return self.api_client.make_request(
            'POST', path=path, data=data, response_type='Vendor')

    def vendors_read(self, vendor_id,  **kwargs):
        """
        vendors_read.

        :param str vendor_id: (required)
        :return: Vendor
        """
        path = f'container-scanning/vendors/{vendor_id}/'

        return self.api_client.make_request('GET', path=path)

    def vendors_list(self,  **kwargs):
        """
        vendors_list.

        :return: list[Vendor]
        """
        path = f'container-scanning/vendors/'

        return self.api_client.make_request(
            'GET', path=path, response_type='list[Vendor]')

    def vendors_search(self, name,  **kwargs):
        """
        vendors_search.

        :param str name: (required)
        :return: list[Vendor]
        """
        path = f'container-scanning/vendors/'
        params = {'name': name}

        return self.api_client.make_request(
            'GET', path=path, params=params, response_type='list[Vendor]')
