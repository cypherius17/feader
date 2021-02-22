import os
from django.urls import path
from .views import (
    RSSItemListView,
    RSSItemDetailView
)

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = [
    path("rss-items/", RSSItemListView.as_view()),
    path("rss-items/create/", RSSItemDetailView.as_view({"post": "post"})),
    path("edit/<int:pk>/", RSSItemDetailView.as_view({"post": "put"})),
    path("delete/<int:pk>/", RSSItemDetailView.as_view({"get": "delete"})),
]
