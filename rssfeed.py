from rfeed import *
from rssbody import RssBody as rb
import datetime

class RssFeed(object):
    def __init__(self,rss_body,entry_link):
        self.rss_body = rss_body
        self.entry_link = entry_link
        self.rss_items = []
        self.rss_feed = Feed("","","")
        self.rss_xml = ""

    async def gen_feed(self):
        if not self.rss_body:
            #print(f"there are no rss_body contents in {self.rss_body}")
            pass
        for entry in self.rss_body:
            #date_str = entry.get("datetime")
            #if date_str is None:
            date_str = datetime.datetime.now()
            #else:
            #    date_str = date_str.strip()
            #    date_str = date_str.replace("-"," ")
            #    my_date = datetime.datetime.strptime(date_str,'%Y %m %d')
            #    if my_date is None:
            #        my_date = datetime.datetime.now()

            item1 = Item(title = entry.get("entry"), #entry title
                         link = entry.get("link"),
                         guid = Guid(entry.get("guid")),
                         description= entry.get("entry_content"),# entry content
                         author = entry.get("author"),
                         pubDate = date_str)
            self.rss_items.append(item1)

        self.rss_feed = Feed(
            title = self.entry_link.other_for_rss.get("site_title"),#site title
            link = self.entry_link.other_for_rss.get("rss_link"), #rss link
            description = self.entry_link.other_for_rss.get("site_motto"),#site motto
            language = "en-US",
            lastBuildDate = datetime.datetime.now(),
            items = self.rss_items
        )

        self.rss_xml = self.rss_feed.rss()

    async def start(self):
    #def start(self):
        await self.gen_feed()
    #    self.get_rss_body()

