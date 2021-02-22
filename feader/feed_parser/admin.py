from django.contrib import admin

from .models import (
    RSSSource,
    RSSItem
)


admin.site.register(RSSSource)
admin.site.register(RSSItem)
