"""Tiny dev-only CORS for http://localhost:3000 (no new library)."""
from django.conf import settings


class DevCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG and request.headers.get("Origin") == "http://localhost:3000":
            response["Access-Control-Allow-Origin"] = "http://localhost:3000"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type"
            if request.method == "OPTIONS":
                response.status_code = 204
        return response
