from unittest import TestCase
from unittest.mock import patch

from src.my_lambda.exception import ServerException


class TestServerException(TestCase):

    @patch('src.my_lambda.exception.ServerException.__init__', return_value=None)
    def test_exception(self, mock_init):
        status_code = 500
        body = {'message': 'Internal Error'}
        mock_init.error_message = {'statusCode': 500, 'body': {'message': 'Internal Error'}}

        exception = ServerException(status_code, body)

        mock_init.assert_called_once_with(status_code, body)
        self.assertEqual("(500, {'message': 'Internal Error'})", str(exception))

