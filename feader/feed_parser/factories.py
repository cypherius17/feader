from .models import RSSItem, RSSSource
from factory import (DjangoModelFactory, SubFactory, lazy_attribute)
from faker import Factory

faker = Factory.create()


class RSSSourceFactory(DjangoModelFactory):
    class Meta:
        model = RSSSource
    title = lazy_attribute(lambda _: faker.sentence())
    link = lazy_attribute(lambda _: faker.url())
    description = lazy_attribute(lambda _: faker.paragraph())
    pub_date = lazy_attribute(lambda _: faker.date_time())
    source_url = lazy_attribute(lambda _: faker.url())


class RSSItemFactory(DjangoModelFactory):
    class Meta:
        model = RSSItem

    title = lazy_attribute(lambda _: faker.sentence())
    link = lazy_attribute(lambda _: faker.url())
    description = lazy_attribute(lambda _: faker.paragraph())
    pub_date = lazy_attribute(lambda _: faker.date_time())
    rss_source = SubFactory(RSSSourceFactory)
    category = lazy_attribute(lambda _: faker.word())
