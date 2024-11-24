from src.my_lambda.directory.dir import Dir
from src.my_lambda.module.mod import Mod
from src.my_lambda.utils import RequestHandlerAPI


def lambda_handler(event, context):
    request_handler = RequestHandlerAPI(event.get('method', ''))
    check_http_method = request_handler.check_http_method()

    if check_http_method is not None:
        return check_http_method

    encode_body = request_handler.encode_body(event)
    response = request_handler.do_request(event, encode_body)
    response_body = request_handler.check_response(response)

    module = Mod()
    module.runnable()

    directory = Dir()
    directory.lister()

    return request_handler.build_response(response, response_body)

