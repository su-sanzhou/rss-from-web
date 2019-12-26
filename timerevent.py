from tornado import ioloop
from entrylink import EntryLink
from rssbody import RssBody
from rssfeed import RssFeed
from rsssql import RssSql
import datetime
import hashlib
import tornado.gen
import time
import asyncio

class TimerEvent(object):
    def __init__(self,mini_interval):
        self.mini_interval = mini_interval #seonds
        self.xpath_id_interval = [] #all xpath_id and interval,inner is tuple
        self.xpath_id_time = {} # all xpath_id and last execute timestamp
        self.xpath_id_rss_sha256sum = {} # all xpath_id and rss shasum
        self.now_stamp = datetime.datetime.now().timestamp()

    async def timer_execute(self):
        rss_sql = RssSql()
        new_stamp = datetime.datetime.now().timestamp()
        #if self.mini_interval == -1:
        self.xpath_id_interval = await rss_sql.get_xpath_id_interval_all()
        for id_interval in self.xpath_id_interval:
            self.xpath_id_time[id_interval["xpath_id"]] = self.now_stamp

        try:
            for id_interval in self.xpath_id_interval:
                if (new_stamp - self.xpath_id_time[id_interval["xpath_id"]]) > id_interval["interval_time"]:
                    self.now_stamp = new_stamp
                    xpath = await rss_sql.get_xpath_one_from_xpath_id(id_interval["xpath_id"])
                    gened_rss = await self.gen_feed_from_xpath(xpath)


                    sha256 = hashlib.sha256()
                    sha256.update(gened_rss.rss_xml.encode('utf-8'))
                    res = sha256.hexdigest()

                    #if res != self.xpath_id_rss_sha256sum[id_interval["xpath_id"]]:
                    await rss_sql.update_one_rss_xpath_id(gened_rss.rss_xml,
                                           res,
                                           id_interval["xpath_id"])
        except:
            print(f"update some url have problem,maybe the url have been shutdown")

        #print(f"mini_interval is: {self.mini_interval}")
        ioloop.IOLoop.current().add_timeout(time.time() + self.mini_interval,
                                            self.timer_execute)

    async def gen_feed_from_xpath(self,xpath):
        entry_link = EntryLink(xpath["site_url"],
                               xpath["entry_css"],
                               xpath["entry_link_css"],
                               xpath["add_base_url"],
                               xpath["rss_link_prefix"],
                               xpath["site_title_css"],
                               xpath["site_motto_css"],
                               xpath["base_url"])
        await entry_link.start() #get entry_and_link,stored in entry_link

        rss_body = RssBody(entry_link.entry_and_link,
                           xpath["entry_content_css"],
                           xpath["author_css"],
                           xpath["datetime_css"])

        await rss_body.get_rss_body() # get rss_body,stored in rss_body

        rss_feed = RssFeed(rss_body.rss_body,entry_link)
        await rss_feed.start()

        return rss_feed





