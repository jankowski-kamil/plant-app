from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail):
        super().__init__(detail, code="invalid")
