from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path


def hello(request):
    return HttpResponse("Hello Al-Shamela Bookstore backend")


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", hello, name="hello"),
    path("health/", health, name="health"),
    path("admin/", admin.site.urls),
]
