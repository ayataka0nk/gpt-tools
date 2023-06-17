from typing import List
from .exceptions import MyHTTPException


def make_responses(errors: List[MyHTTPException]):
    responses = {}
    for error in errors:
        responses[error.status_code] = {
            "description": error.description,
            "model": error.model
        }
    return responses
