import logging
import feedparser
from datetime import datetime
from feed_parser.models import RSSSource, RSSItem

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class FeedUtils:
    @staticmethod
    def datetime_from_pub_date(pub_date):
        if not pub_date:
            return None
        return datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")

    @staticmethod
    def write_to_log_file(log_file, log):
        with open(log_file, 'a') as f:
            f.write(log)

    @staticmethod
    def handle_rss_items_result(items, rss_source):
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

    @staticmethod
    def handle_rss_source_result(feed, source_url):
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

    @staticmethod
    def fetch_rss_elements(source_urls):
        source_urls = list(set(source_urls))
        for url in source_urls:
            response = feedparser.parse(url)
            rss_source = FeedUtils.handle_rss_source_result(response.feed, url)
            FeedUtils.handle_rss_items_result(response.entries, rss_source)
