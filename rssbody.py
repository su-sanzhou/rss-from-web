from entrylink import EntryLink
from lxml import etree
from lxml import html as lhtml


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


    async def get_rss_body(self):
        #if not self.entry_and_link:
        for entry in self.entry_and_link:
            #if not entry:
            #    print(f"there are no entry in entry_and_link:{self.entry_and_link}")

            link = self.entry_and_link[entry]
            #if not link:
            #    print(f"there are no link in entry_and_link:{self.entry_and_link}")

            # just want to use EntryLink.get_http_body
            entry_link = EntryLink(link,self.entry_content_css,
                            self.author_css, False,
                            "nothing","nothing","nothing","base_url")
            http_body = await entry_link.get_http_body(link)

            if entry_link.status["status_http_body"] != self.do_success:
                temp_entry_link = {"entry": entry, "link": link,
                                   "entry_content": " ",
                                   "author": " ",
                                   "datetime": " ",
                                   "guid": f'Guid("{link}")'}
                self.rss_body.append(temp_entry_link)
                entry_link.all_status = self.do_success
                self.all_status = self.do_success

            else:

                #file = open("douban.html","w")
                #file.write(http_body)
                #file.close()


                http_html = lhtml.fromstring(http_body)

                #if not http_html:
                #    print(f"there are no contents in http_html:{http_html}")

                entry_content = await self.get_entry_content(http_html,
                                                       self.entry_content_css)
                author = await  self.get_rss_author(http_html, self.author_css)
                datetime = await  self.get_rss_datetime(http_html, self.datetime_css)

                temp_entry_link = {"entry": entry, "link": link,
                                   "entry_content": entry_content,
                                   "author": author,
                                   "datetime": datetime,
                                   "guid": f'Guid("{link}")'}
                self.rss_body.append(temp_entry_link)

    async def get_entry_content(self, http_html,entry_content_css):
        #print(f"the entry_conten_css is:{entry_content_css}")
        entry_contents = http_html.xpath(entry_content_css)
        string_entry_content = ""
        if not entry_contents:
            #print(f"there are no contents in entry_contents:{entry_contents}")
            self.status["status_entry_centent"] = f"No contents for every {entry_content_css}"
        else:
            for entry_content in entry_contents:
                string_entry_content += bytes.decode(etree.tostring(entry_content))

            if not string_entry_content:
                #print(f"there are no contents in string_entry_content:{string_entry_content}")
                self.status["status_entry_centent"]  = f"No contents for every {entry_contents}"

        return string_entry_content

    async def get_rss_author(self, http_html,  author_css):
        author_all = http_html.xpath(author_css)
        if not author_all:
            #self.status["status_rss_author"] = f"there are no author in author_all:{author_all}"
            return ""
        else:
            return author_all[0].text

    async def get_rss_datetime(self, http_html,  datetime_css):
        datetime_all = http_html.xpath(datetime_css)
        if not datetime_all:
            #self.status["status_rss_datetime"] = f"there are no datetime in datetime_all:{datetime_all}"
            return ""
        else:
            return datetime_all[0].text

    async def start(self):
        await self.get_rss_body()
        if self.status["status_rss_body"] != self.do_success \
            or self.status["status_entry_content"] != self.do_success \
            or self.status["status_rss_author"] != self.do_success:
            self.all_status = self.do_not_success

