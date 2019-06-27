import flask
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code: int, message: str = None) -> flask.Response:
    """Custom error response.

    Args:
        status_code: Status code of the error response.
        message: Message for the error response.

    Returns:
        Flask error response.
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message: str) -> flask.Response:
    """400 error response.

    Args:
        message: Message of the error response.

    Returns:
        400 error response.
    """
    return error_response(400, message)
