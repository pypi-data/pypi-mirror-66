import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from ccvs_scanning_api_client.api_client import ApiClient
from ccvs_scanning_api_client.configuration import Configuration
from ccvs_scanning_api_client.models import Vendor


class TestApiClient(unittest.TestCase):
    """ApiClient unit test stubs."""

    def setUp(self):
        config = Configuration(host='http://localhost')
        self.api = ApiClient(config)

    def tearDown(self):
        pass

    @patch('ccvs_scanning_api_client.api_client.request')
    def test_make_request_get_vendor(self, mock):
        """Test case for make_request_get_vendor."""
        vendor = {
            'id': 1,
            'name': 'name123',
            'credentials': {'config': {}}
        }
        vendor_obj = Vendor(**vendor)
        json = MagicMock(return_value=vendor)
        mock.return_value = MagicMock(json=json, status_code=200)
        response = self.api.make_request(
            'GET', 'container-scanning/vendors/', response_type='Vendor')

        mock.assert_called_with(
            'GET',
            'http://localhost/container-scanning/vendors/',
            data=None,
            headers={'Content-Type': 'application/json'},
            params=None
        )

        self.assertEqual(response, vendor_obj)


if __name__ == '__main__':
    unittest.main()
