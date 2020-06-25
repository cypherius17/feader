import pytz
from faker import Factory
from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from .models import RSSItem, RSSSource
from .factories import RSSSourceFactory, RSSItemFactory
from .utils.feed_utils import FeedUtils

faker = Factory.create()


class RSSTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = '/rss-items/create/'
        self.edit_url = '/edit/{}/'
        self.delete_url = '/delete/{}/'
        self.rss_source_factory = RSSSourceFactory()

    def test_create_rss_item(self):
        data = {
            'title': faker.sentence(),
            'link': faker.url(),
            'description': faker.paragraph(),
            'pub_date': faker.date_time().isoformat(),
            'rss_source': self.rss_source_factory.id,
            'guid': faker.word(),
            'category': faker.word(),
            'comments': faker.sentence()
        }
        self.client.post(self.create_url, data=data)
        check_query = RSSItem.objects.filter(
            title=data['title'],
            link=data['link'],
            description=data['description'],
            pub_date=data['pub_date'],
            rss_source=data['rss_source'],
            guid=data['guid'],
            category=data['category'],
            comments=data['comments']
        )
        assert check_query.exists()
        assert check_query.count() == 1

    def test_edit_rss_item(self):
        rss_item = RSSItemFactory()
        data = {
            'title': faker.sentence(),
            'rss_source': RSSSourceFactory().id
        }
        self.client.post(self.edit_url.format(rss_item.id), data=data)
        rss_item = RSSItem.objects.get(id=rss_item.id)
        assert rss_item.title == data['title']
        assert rss_item.rss_source.id == data['rss_source']

    def test_delete_rss_item(self):
        rss_item = RSSItemFactory()
        self.client.get(self.delete_url.format(rss_item.id))
        assert not RSSItem.objects.filter(id=rss_item.id).exists()


class FetchUtilTestCase(TestCase):
    def setUp(self):
        self.sample_rss_urls = [
            'https://www.feedforall.com/sample.xml',
            'https://www.feedforall.com/blog-feed.xml'
        ]

    def test_fetch_function_single_url(self):
        FeedUtils.fetch_rss_elements([self.sample_rss_urls[0]])
        rss_source_query = RSSSource.objects.filter(
            title='FeedForAll Sample Feed',
            link='http://www.feedforall.com/industry-solutions.htm',
            description='RSS is a fascinating technology. The uses for RSS are expanding daily. Take a closer look at how various industries are using the benefits of RSS in their businesses.',
            source_url=self.sample_rss_urls[0],
            pub_date=datetime(2004, 10, 19, 17, 38, 55, 0, pytz.UTC)
        )
        rss_item_query = RSSItem.objects.all()

        assert rss_source_query.exists()
        assert rss_item_query.count() == 9

    def test_fetch_function_multi_urls(self):
        FeedUtils.fetch_rss_elements(self.sample_rss_urls)
        rss_source_query = RSSSource.objects.all()
        rss_item_query = RSSItem.objects.all()
        assert rss_item_query.count() == 745
        assert rss_source_query.count() == 2

    def test_fetch_function_get_or_create(self):
        FeedUtils.fetch_rss_elements([self.sample_rss_urls[0]])
        FeedUtils.fetch_rss_elements([self.sample_rss_urls[0]])
        rss_source_query = RSSSource.objects.all()
        rss_item_query = RSSItem.objects.all()
        assert rss_source_query.count() == 1
        assert rss_item_query.count() == 9
