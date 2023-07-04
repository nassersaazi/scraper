import uuid
from .utils import strip_tags, strip_attributes
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BtcphilosophySpider(CrawlSpider):
    name = "btcphilosophy"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/bitcoin-dev-philosophy/btcphilosophy"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//span/a[contains(@href, 'adoc')]"),
            callback="parse_item",
        ),
    )

    def parse_item(self, response):
        item = {}
        article = response.xpath("//article").get()
        item["id"] = "btcphilosophy-" + str(uuid.uuid4())
        item["title"] = "[Bitcoin Dev Philosopy] " + response.xpath("//article/div/h2/text()").get()

        if not item["title"]:
            return None

        item["body_formatted"] = strip_attributes(article)
        item["body"] = strip_tags(article)
        item["body_type"] = "html"
        item["authors"] = ["Kalle Rosenbaum", "Linnéa Rosenbaum"]
        item["domain"] = self.start_urls[0]
        item["url"] = response.url
        item["created_at"] = datetime.now()

        return item