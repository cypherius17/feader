from datetime import datetime
from rest_framework import serializers

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from .models import RSSSource, RSSItem


class RSSSourceSerializer(ModelSerializer):
    class Meta:
        model = RSSSource
        fields = "__all__"
        read_only_fields = ("id",)


class RSSItemSerializer(ModelSerializer):
    source_title = SerializerMethodField()
    formatted_pub_date = SerializerMethodField()

    class Meta:
        model = RSSItem
        fields = "__all__"
        read_only_fields = ("id",)

    def get_source_title(self, obj):
        return obj.rss_source.title

    def get_formatted_pub_date(self, obj):
        return datetime.strftime(obj.pub_date, '%d/%m/%Y %H:%M') if obj.pub_date else ''
