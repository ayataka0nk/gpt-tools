from .exceptions import MyHTTPException


def make_responses(errors: list[MyHTTPException]):
    responses = {}
    for error in errors:
        responses[error.status_code] = {
            "description": error.description,
            "model": error.model
        }
    return responses
