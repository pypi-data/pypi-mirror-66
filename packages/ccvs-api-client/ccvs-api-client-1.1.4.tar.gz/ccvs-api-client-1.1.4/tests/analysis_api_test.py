import unittest
from unittest.mock import MagicMock

from ccvs_scanning_api_client.api.analysis_api import AnalysisApi


class TestAnalysisApi(unittest.TestCase):
    """AnalysisApi unit test stubs."""

    def setUp(self):
        self.mock = MagicMock()
        self.mock.make_request.return_value = 'Mock'
        self.api = AnalysisApi(self.mock)

    def tearDown(self):
        pass

    def test_analysis_create(self):
        """Test case for analysis_create."""
        self.api.analysis_create('image')
        self.api.api_client.make_request.call_args(
            'POST',
            'container-scanning/analysis/',
            image='image',
            response_type='Analysis')

    def test_analysis_read(self):
        """Test case for analysis_read."""
        self.api.analysis_read('abc123')
        self.api.api_client.make_request.call_args(
            'GET',
            'container-scanning/analysis/abc123',
            response_type='Analysis')


if __name__ == '__main__':
    unittest.main()
