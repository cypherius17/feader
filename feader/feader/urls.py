from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("feed_parser.urls", namespace="feed_parser")),
]
