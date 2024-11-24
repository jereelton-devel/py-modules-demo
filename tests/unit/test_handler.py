from unittest import TestCase
from unittest.mock import patch, Mock

from src.my_lambda.handler import lambda_handler
from tests.source import DataSource, Messages


class TestLambdaFunction(TestCase):

    def test_lambda_handler_no_mocking(self):
        result = lambda_handler(DataSource.do_request_ok(), None)
        self.assertEqual(DataSource.response_body_ok_12070020(), result["body"])


    def test_lambda_handler_no_mocking_405(self):
        result = lambda_handler(DataSource.do_request_405(), None)
        self.assertEqual(Messages.MSG_405_METHOD.value, result)


    @patch('src.my_lambda.utils.requests.request')
    @patch('src.my_lambda.utils.RequestHandlerAPI.build_response')
    def test_lambda_handler_mocking_parts(self, mock_build_response, mock_requests):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"key": "value"}'
        mock_response.headers = {}
        mock_response.json.return_value = DataSource.response_ok()
        mock_requests.return_value = mock_response

        mock_build_response.return_value = {'statusCode': 200, 'body': 'mocked_response_body'}

        result = lambda_handler(event=DataSource.do_request_ok(), context=None)
        self.assertEqual({'statusCode': 200, 'body': 'mocked_response_body'}, result)


    @patch('src.my_lambda.utils.RequestHandlerAPI.check_http_method')
    @patch('src.my_lambda.utils.RequestHandlerAPI.encode_body')
    @patch('src.my_lambda.utils.RequestHandlerAPI.do_request')
    @patch('src.my_lambda.utils.RequestHandlerAPI.check_response')
    @patch('src.my_lambda.utils.RequestHandlerAPI.build_response')
    def test_lambda_handler_mocking(self, mock_build_response, mock_check_response, mock_do_request, mock_encode_body, mock_check_method):
        mock_check_method.return_value = None
        mock_encode_body.return_value = {}
        mock_do_request.return_value = {}
        mock_check_response.return_value = {}
        mock_build_response.return_value = {}

        result = lambda_handler(event=DataSource.do_request_ok(), context=None)
        self.assertEqual({}, result)


    @patch('src.my_lambda.utils.RequestHandlerAPI.check_http_method')
    @patch('src.my_lambda.utils.RequestHandlerAPI.encode_body')
    @patch('src.my_lambda.utils.RequestHandlerAPI.do_request')
    @patch('src.my_lambda.utils.RequestHandlerAPI.check_response')
    @patch('src.my_lambda.utils.RequestHandlerAPI.build_response')
    def test_lambda_handler_mocking_405(self, mock_build_response, mock_check_response, mock_do_request, mock_encode_body, mock_check_method):
        mock_check_method.return_value = Messages.MSG_405_METHOD.value
        mock_encode_body.return_value = {}
        mock_do_request.return_value = {}
        mock_check_response.return_value = {}
        mock_build_response.return_value = {}

        result = lambda_handler(event=DataSource.do_request_ok(), context=None)
        self.assertEqual(Messages.MSG_405_METHOD.value, result)

