import feedparser
import logging

from django.core.management.base import BaseCommand
from feed_parser.utils.feed_utils import FeedUtils

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

    def handle(self, *args, **options):
        logger.info("Start fetching rss...")
        source_urls = options.get("feed_urls").split(',')
        FeedUtils.fetch_rss_elements(source_urls)
        logger.info("Done!")
