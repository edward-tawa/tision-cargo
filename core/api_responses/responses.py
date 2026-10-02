# core/responses.py
from rest_framework.response import Response


def success_response(*, message, status, data=None):
    return Response(
        {"success": True, "message": message, "data": data},
        status=status,
    )


def error_response(*, message, status, errors=None):
    return Response(
        {"success": False, "message": message, "errors": errors},
        status=status,
    )
