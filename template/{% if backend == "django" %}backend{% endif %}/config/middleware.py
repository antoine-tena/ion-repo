"""Permissions-Policy header ([SECURITY-HEADERS]), which Django does not set itself."""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

# Browser features refused to every page: open them one by one, when needed.
PERMISSIONS_POLICY = "camera=(), geolocation=(), microphone=(), payment=(), usb=()"


class PermissionsPolicyMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        response.headers.setdefault("Permissions-Policy", PERMISSIONS_POLICY)
        return response
