from django.db import models
from feader.models import TimeStamp
from feader.constants import (
    SHORT_TEXT_LENGTH
)


# Create your models here.
class RSSAbstractModel(models.Model):
    title = models.CharField(
        null=True,
        blank=True,
        max_length=SHORT_TEXT_LENGTH
    )
    link = models.CharField(
        null=True,
        blank=True,
        max_length=SHORT_TEXT_LENGTH
    )
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class RSSSource(TimeStamp, RSSAbstractModel):
    source_url = models.CharField(max_length=SHORT_TEXT_LENGTH)

    def __str__(self):
        return "{} ({})".format(self.title, self.source_url)


class RSSItem(TimeStamp, RSSAbstractModel):
    rss_source = models.ForeignKey(RSSSource, on_delete=models.CASCADE)
    guid = models.CharField(
        null=True,
        blank=True,
        max_length=SHORT_TEXT_LENGTH
    )
    category = models.CharField(
        null=True,
        blank=True,
        max_length=SHORT_TEXT_LENGTH
    )
    comments = models.CharField(
        null=True,
        blank=True,
        max_length=SHORT_TEXT_LENGTH
    )

    def __str__(self):
        return "{} > {}".format(self.rss_source.title, self.title)
