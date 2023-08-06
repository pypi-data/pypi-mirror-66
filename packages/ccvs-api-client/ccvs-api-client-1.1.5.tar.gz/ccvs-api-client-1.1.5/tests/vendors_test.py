import unittest
from unittest.mock import MagicMock

from ccvs_scanning_api_client.api import vendors_api


class TestVendorsAPI(unittest.TestCase):
    """VendorsAPI unit test stubs."""

    def setUp(self):
        self.mock = MagicMock()
        self.mock.make_request.return_value = 'Mock'
        self.api = vendors_api.VendorsApi(
            self.mock)

    def tearDown(self):
        pass

    def test_vendors_create(self):
        """Test case for vendors_create."""
        self.api.vendors_create('data')
        self.api.api_client.make_request.call_args(
            'POST',
            'container-scanning/vendors/',
            data='data',
            response_type='Vendor')

    def test_vendors_list(self):
        """Test case for vendors_list."""
        self.api.vendors_list()
        self.api.api_client.make_request.call_args(
            'GET',
            'container-scanning/vendors/',
            response_type='list[Vendor]')

    def test_vendors_search(self):
        """Test case for vendors_search."""
        params = {'name': 'name123'}
        self.api.vendors_search(name='name123')
        self.api.api_client.make_request.call_args(
            'GET',
            'container-scanning/vendors/',
            params=params,
            response_type='list[Vendor]')

    def test_vendors_read(self):
        """Test case for vendors_read."""
        self.api.vendors_read('abc123')
        self.api.api_client.make_request.call_args(
            'GET',
            'container-scanning/vendors/abc123',
            response_type='Vendor')


if __name__ == '__main__':
    unittest.main()
