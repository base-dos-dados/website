from scrapy.item import Field, Item
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule


class LinkStatus(Item):
    url = Field()
    status = Field()
    referer = Field()
    link_text = Field()


class LinkSpider(CrawlSpider):
    name = "link-checker"
    report_if = set(range(400, 600))
    handle_httpstatus_list = list(report_if)
    
    # Send referrer headers to every URL
    custom_settings = {
        "REFERRER_POLICY": "unsafe-url"
    }

    start_urls = [
        "https://basedosdados.org/",
        "https://basedosdados.org/dataset/",
        "https://basedosdados.org/organization/",
        "https://basedosdados.org/group/",
        "https://basedosdados.org/about",
    ]

    # Test regex rules with
    # https://regex101.com/
    rules = [
        Rule(
            # Deny links with more than one question mark with
            #   "(?<!\?)\?(?!\?)"
            # Deny https://basedosdados.org/<entity>/activity/ pages with
            #   ".*\/activity\/.*"
            #   ".*\/activity_id.*"
            #   ".*\/dataset\/changes\/.*"
            # Allow only https://basedosdados.org/ pages with
            #   "basedosdados\.org.*"
            LinkExtractor(
                deny=[
                    "(?<!\?)\?(?!\?)",
                    ".*\/activity\/.*",
                    ".*\/activity_id.*",
                    ".*\/dataset\/changes\/.*",
                ],
                allow="basedosdados\.org.*",
            ),
            callback="parse",
            follow=True,
        ),
        Rule(
            # Deny https://basedosdados.org/ pages with
            #   "basedosdados\.org.*"
            LinkExtractor(deny=["basedosdados\.org.*"]),
            callback="parse",
            follow=False,
        ),
    ]

    def parse(self, response):
        if response.status in self.report_if:
            item = LinkStatus()
            item["url"] = response.url
            item["status"] = response.status
            item["link_text"] = self._format(response.meta["link_text"])
            item["referer"] = response.request.headers.get(
                "Referer", "https://no.referer"
            )
            yield item
        yield None

    def _format(self, line):
        return " ".join(line.strip().split())


# References
# https://gist.github.com/mdamien/7b71ef06f49de1189fb75f8fed91ae82
# https://matthewhoelter.com/2018/11/27/finding-broken-links-on-website.html
# https://dev.to/pjcalvo/broken-links-checker-with-python-and-scrapy-webcrawler-1gom
