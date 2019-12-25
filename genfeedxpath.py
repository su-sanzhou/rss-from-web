from entrylink import EntryLink
from rssbody import RssBody
from rssfeed import RssFeed

class GenFeedXpath(object):

    async def gen_feed_from_xpath(self, xpath):
        entry_link = EntryLink(xpath["site_url"],
                               xpath["entry_css"],
                               xpath["entry_link_css"],
                               xpath["add_base_url"],
                               xpath["rss_link_prefix"],
                               xpath["site_title_css"],
                               xpath["site_motto_css"])
        await entry_link.start()  # get entry_and_link,stored in entry_link

        rss_body = RssBody(entry_link.entry_and_link,
                           xpath["entry_content_css"],
                           xpath["author_css"],
                           xpath["datetime_css"])

        await rss_body.get_rss_body()  # get rss_body,stored in rss_body

        rss_feed = RssFeed(rss_body.rss_body, entry_link)
        gened_rss = await rss_feed.start()

        return gened_rss




