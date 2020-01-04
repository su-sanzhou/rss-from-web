from entrylink import EntryLink
from lxml import etree
from lxml import html as lhtml
from rsslog import RssLog

class RssBody(object):
    def __init__(self, entry_and_link,entry_content_css,
                 author_css, datetime_css):
        self.entry_and_link = entry_and_link
        self.rss_body = []
        self.entry_content_css = entry_content_css
        self.author_css = author_css
        self.datetime_css = datetime_css
        self.do_success = "do_success"
        self.do_not_success = "do_not_success"
        self.status = {"status_rss_body": self.do_success,
                       "status_entry_content": self.do_success,
                       "status_rss_author": self.do_success}
        self.all_status = self.do_success
        self.rss_logger = RssLog()

    async def get_rss_body(self):
        print("1")
        for entry in self.entry_and_link:
            link = self.entry_and_link[entry]
            print("2")
            entry_link = EntryLink(link,self.entry_content_css,
                            self.author_css, False,
                            "nothing","nothing","nothing","base_url")
            http_body = await entry_link.get_http_body(link)

            if entry_link.status["status_http_body"] != self.do_success:
                # this branch just give an empty entry_content
                temp_entry_link = {"entry": entry, "link": link,
                                   "entry_content": " ",
                                   "author": " ",
                                   "datetime": " ",
                                   "guid": f'Guid("{link}")'}
                self.rss_body.append(temp_entry_link)
                entry_link.all_status = self.do_success
                self.all_status = self.do_success
                print("3")
            else:
                print("4")
                http_html = etree.HTML(http_body)
                print("5")
                entry_content = await self.get_entry_content(http_html,
                                                       self.entry_content_css)
                print("6")
                author = await  self.get_rss_author(http_html, self.author_css)
                print("7")
                datetime = await  self.get_rss_datetime(http_html, self.datetime_css)
                print("8")
                temp_entry_link = {"entry": entry, "link": link,
                                   "entry_content": entry_content,
                                   "author": author,
                                   "datetime": datetime,
                                   "guid": f'Guid("{link}")'}
                self.rss_body.append(temp_entry_link)
                print("9")

    async def get_entry_content(self, http_html,entry_content_css):
        entry_contents = http_html.xpath(entry_content_css)
        string_entry_content = ""
        if len(entry_contents) == 0:
            log_info = f"can not parse contents from entry_contents using {entry_content_css}"
            self.rss_logger.rss_logger.info(log_info)
            self.status["status_entry_centent"] = f"No contents for every {entry_content_css}"
        else:
            for entry_content in entry_contents:
                string_entry_content += etree.tostring(entry_content,encoding = "utf-8").decode(encoding="utf-8")
                #string_entry_content += bytes.decode(etree.tostring(entry_content))

            if not string_entry_content:
                log_info = f"there are no contents in string_entry_content:{string_entry_content}"
                self.rss_logger.rss_logger.info(log_info)
                self.status["status_entry_centent"]  = f"No contents for every {entry_contents}"

        return string_entry_content

    async def get_rss_author(self, http_html,  author_css):
        author_all = http_html.xpath(author_css)
        if len(author_all) == 0:
            log_info = f"can not parse author from author_all using {author_css}"
            self.rss_logger.rss_logger.info(log_info)
            return ""
        else:
            return etree.tostring(author_all[0], method="text", encoding="utf-8").decode(encoding="utf-8")

    async def get_rss_datetime(self, http_html,  datetime_css):
        datetime_all = http_html.xpath(datetime_css)
        if len(datetime_all) == 0:
            log_info = f"can not parse datetime from http_html using {datetime_css}"
            self.rss_logger.rss_logger.info(log_info)
            return ""
        else:
            return etree.tostring(datetime_all[0], method="text", encoding="utf-8").decode(encoding="utf-8")

    async def start(self):
        await self.get_rss_body()
        if self.status["status_rss_body"] != self.do_success \
            or self.status["status_entry_content"] != self.do_success \
            or self.status["status_rss_author"] != self.do_success:
            self.all_status = self.do_not_success

