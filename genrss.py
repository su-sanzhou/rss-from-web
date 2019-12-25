from entrylink import EntryLink
from rssbody import RssBody
from rssfeed import RssFeed
from rsssql import RssSql
import datetime
import hashlib

class GenRss(object):
    def __init__(self):
        pass

    async def gen_insert_rss(self,site_url,entry_css,entry_link_css,
                             add_base_url,rss_link_prefix,
                             site_title_css,site_motto_css,#for entry_link
                             entry_content_css,author_css,
                             datetime_css,# for rss_body
                             user_id,xpath_id,rss_url_name,# for insert rss
                             interval_time # for insert xpath
                             )
        entry_link = EntryLink(site_url,entry_css,entry_link_css,
                               add_base_url,rss_link_prefix,
                               site_title_css,site_motto_css)
        await entry_link.start()

        rss_body = RssBody(entry_link.entry_and_link,
                           entry_content_css,author_css,
                           datetime_css)

        await rss_body.get_rss_body()

        rss_feed = RssFeed(rss_body.rss_body,entry_link)
        gened_rss = await rss_feed.gen_feed()


        sha256 = hashlib.sha256()
        sha256.update(gened_rss.encode('utf-8'))
        res = sha256.hexdigest()

        rss_sql = RssSql()

        await rss_sql.insert_rss(user_id,
                           xpath_id,
                           entry_link.other_for_rss.get("site_title"),
                           rss_url_name,
                           gened_rss,
                           datetime.datetime.now(),
                           res)

        await rss_sql.insert_xpath(user_id,site_url,entry_css,
                             entry_link_css,add_base_url,
                             rss_link_prefix,site_title_css,
                             site_motto_css,entry_content_css,
                             author_css,datetime_css,
                             interval_time)
