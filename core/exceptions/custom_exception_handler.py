# core/exceptions/custom_exception_handler.py
from django.core.exceptions import ObjectDoesNotExist
from loguru import logger
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import exception_handler

from core.api_responses.responses import error_response


def custom_exception_handler(exc, context):
    # Convert Django's DoesNotExist into DRF's NotFound exception globally
    if isinstance(exc, ObjectDoesNotExist):
        exc = NotFound("Requested resource not found.")

    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "message": "Validation or request error.",
            "errors": response.data,
        }
    else:
        logger.exception(f"Unhandled server error: {exc}")
        return error_response(
            message="An unexpected server error occurred.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors={"detail": str(exc)},
        )

    return response
