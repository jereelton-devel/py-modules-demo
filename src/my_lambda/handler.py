from src.my_lambda.utils import RequestHandlerAPI


def lambda_handler(event, context):
    request_handler = RequestHandlerAPI(event.get('method', ''))
    request_handler.check_http_method()
    encode_body = request_handler.encode_body(event)
    response = request_handler.do_request(event, encode_body)
    response_body = request_handler.check_response(response)
    return request_handler.build_response(response, response_body)

