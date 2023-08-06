from rest_framework.views import exception_handler
from rest_framework import serializers
# from rest_framework import status
# from rest_framework.response import Response
from django.core.exceptions import ValidationError


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = serializers.ValidationError(exc.message_dict)

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        return response
