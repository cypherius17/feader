import feedparser
import logging

from django.core.management.base import BaseCommand
from feed_parser.models import RSSSource, RSSItem
from feed_parser.feed_utils import FeedUtils

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "feed_urls",
            help='Feed urls (separated by commas) to fetch',
        )

    def handle_rss_source_result(self, feed, source_url):
        try:
            rss_source, is_created = RSSSource.objects.get_or_create(
                title=feed.get('title'),
                link=feed.get('link'),
                source_url=source_url,
                description=feed.get('subtitle'),
                defaults={
                    'pub_date': FeedUtils.datetime_from_pub_date(
                        feed.get('published')
                    )
                }
            )
            logs_by_created_status = {
                True: "Created RSS Source: {}".format(
                        rss_source.title,
                    ),
                False: "RSS Source {} already existed in database. Skipped.".format(
                        rss_source.title,
                    )
            }
            logger.info(
                logs_by_created_status[is_created]
            )
            return rss_source
        except Exception as e:
            logger.exception(e)
            raise

    def handle_rss_items_result(self, items, rss_source):

        for item in items:
            try:
                rss_item, is_created = RSSItem.objects.get_or_create(
                    title=item.get('title'),
                    link=item.get('link'),
                    description=item.get('description'),
                    defaults={
                        'guid': item.get('guid'),
                        'category': item.get('category'),
                        'comments': item.get('comments'),
                        'rss_source': rss_source,
                        'pub_date': FeedUtils.datetime_from_pub_date(
                            item.get('published')
                        )
                    }
                )
                logs_by_created_status = {
                    True: "Created RSS Item: {}".format(
                            rss_item.title,
                        ),
                    False: "RSS Item {} already existed in database. Skipped.".format(
                            rss_item.title,
                        )
                }

                logger.info(
                    logs_by_created_status[is_created]
                )
            except Exception as e:
                logger.exception(e)
                raise


    def fetch_rss_elements(self, source_urls):
        source_urls = list(set(source_urls))
        for url in source_urls:
            response = feedparser.parse(url)
            rss_source = self.handle_rss_source_result(response.feed, url)
            self.handle_rss_items_result(response.entries, rss_source)

    def handle(self, *args, **options):
        logger.info("Start fetching rss...")
        source_urls = options.get("feed_urls").split(',')
        self.fetch_rss_elements(source_urls)
        logger.info("Done!")
