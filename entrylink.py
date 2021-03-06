from tornado import httpclient as hc
from lxml import etree
from lxml import objectify
from urllib.parse import urlparse
import string
import random
from rsslog import RssLog

class EntryLink(object):
    def __init__(self,site_url,entry_css,entry_link_css,
                 add_base_url,rss_link_prefix,
                 site_title_css,site_motto_css,base_url):
        self.site_url = site_url
        self.entry_css = entry_css
        self.entry_link_css = entry_link_css
        self.add_base_url = add_base_url
        self.rss_link_prefix = rss_link_prefix
        self.site_title_css = site_title_css
        self.site_motto_css = site_motto_css
        self.entry_and_link = {}
        self.other_for_rss = {}
        self.base_url = base_url
        self.do_success = "do_success"
        self.do_not_success = "do_not_success"
        self.status = {"status_http_body": self.do_success,
                       "status_entry": self.do_success,
                       "status_entry_link": self.do_success,
                       "status_entry_and_entry_link": self.do_success}
        self.all_status = self.do_success
        self.rss_logger = RssLog()


    async def get_http_body(self,site_url):
        http_user_agent = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'}
        http_request = hc.HTTPRequest(url = site_url,
                                      method = 'GET',
                                      headers = http_user_agent,
                                      connect_timeout = 2000,
                                      request_timeout = 6000)
        http_client = hc.AsyncHTTPClient()
        try:
            response = await http_client.fetch(http_request)
        except Exception as e:
            #add it as a log later
            status_http_body = f"can not get content from site_url:{site_url},the Error is{e}"
            self.rss_logger.rss_logger.info(status_http_body)

            self.status["status_http_body"] = status_http_body
        else:
            if not response:
                log_info = f"there is no content in site_url:{site_url}"
                self.rss_logger.rss_logger.info(log_info)
            return response.body.decode()

    async def get_entry_and_link(self,body,entry_css,entry_link_css,
                           add_base_url,base_url):
        #html = etree.HTML(body)
        #html = etree.XML(body)
        parser = etree.XMLParser(recover=True, ns_clean=True)
        xml = etree.fromstring(body.encode(), parser)
        tree = etree.ElementTree(xml)
        html = tree.getroot()
        for elem in html.getiterator():
            if not hasattr(elem.tag, 'find'): continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i + 1:]
        objectify.deannotate(html, cleanup_namespaces=True)

        entrys = await self.get_entry(html,entry_css)
        entry_links = await  self.get_entry_link(html,entry_link_css,add_base_url,base_url)
        entry_and_link = {}
        if len(entrys) != len(entry_links):
            #add to log later
            log_info = f"the wrong title css or wrong link css"
            self.rss_logger.rss_logger.info(log_info)
            self.status["status_entry_and_entry_link"] = f"the wrong title css or wrong link css"
        else:
            for i in range(len(entrys)):
                entry_and_link[entrys[i]] = entry_links[i]
            return entry_and_link

    async def get_entry(self,html,entry_css):
        entrys = html.xpath(entry_css)
        if len(entrys) == 0:
            log_info = f"there are no contents in entrys: {entrys}"
            self.rss_logger.rss_logger.info(log_info)
            self.status["status_entry"] = f"Can not get entry from {entry_css}"

        entry_list = []

        for entry in entrys:
            entry_list.append(etree.tostring(entry, method="text", encoding="utf-8").decode(encoding="utf-8"))
        return entry_list

    async def get_entry_link(self,html,entry_link_css,add_base_url,base_url):
        entry_links = html.xpath(entry_link_css)
        if len(entry_links) == 0:
            log_info = f"there are no contents in entry_links: {entry_links}"
            self.rss_logger.rss_logger.info(log_info)
            self.status["status_entry_link"] = f"Can not get entry link from {entry_link_css}"
        entry_link_list = []

        for entry_link in entry_links:
            href = entry_link.attrib["href"]
            if not href:
                log_info = f"there are no href in {href}"
                self.rss_logger.rss_logger.info(log_info)
                self.status["status_entry_link"] = f"Can not get the href attr from the {entry_link_css}"
            if add_base_url:
                base_and_href = base_url + href
                undup_base_and_href = base_and_href.replace("//","/")
                if "http://" in base_url:
                    add_http_or_https_url = undup_base_and_href.replace("http:/","http://")
                elif "https://" in base_url:
                    add_http_or_https_url = undup_base_and_href.replace("https:/","https://")
                else:
                    log_info = "something wrong hanppened when get the url"
                    self.rss_logger.rss_logger.info(log_info)
                    self.status["status_entry_link"] = f"Something wrong happened when add base url:{base_url}"
                entry_link_list.append(add_http_or_https_url)
            else:
                entry_link_list.append(href)

        return entry_link_list

    async def get_other(self,http_body,rss_link_prefix,site_url,
                  site_title_css,site_motto_css):
        #html = etree.HTML(http_body)
        #html = etree.XML(http_body)

        parser = etree.XMLParser(recover=True, ns_clean=True)
        xml = etree.fromstring(http_body.encode(), parser)
        tree = etree.ElementTree(xml)
        html = tree.getroot()
        for elem in html.getiterator():
            if not hasattr(elem.tag, 'find'): continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i + 1:]
        objectify.deannotate(html, cleanup_namespaces=True)

        site_title = html.xpath(site_title_css)
        if len(site_title) == 0:
            if "/" not in site_title_css:
                self.other_for_rss["site_title"] = site_title_css
            else:
                log_info = f"there are no site_tile"
                self.rss_logger.rss_logger.info(log_info)
                self.other_for_rss["site_title"] = "no_site_title"
        else:
            res = etree.tostring(site_title[0], method="text", encoding="utf-8").decode(encoding="utf-8")
            self.other_for_rss["site_title"] = res

        site_motto = html.xpath(site_motto_css)
        if len(site_motto) == 0:
            if "/" not in site_motto_css:
                self.other_for_rss["site_motto"] = site_motto_css
            else:
                self.other_for_rss["site_motto"] = " "
        else:
            res = etree.tostring(site_motto[0], method="text", encoding="utf-8").decode(encoding="utf-8")
            self.other_for_rss["site_motto"] = res
#        parse_url = urlparse(site_url)
#        if not parse_url:
#            log_info = f"there are no contents in parse_url: {parse_url}"
#            self.rss_logger.rss_logger.info(log_info)
#        domain = '{uri.netloc}'.format(uri = parse_url)
#        domain = domain.split(".")
        domain = site_url.replace("/","")
        domain = domain.replace("http:","")
        domain = domain.replace("https:","")
        domain = domain.replace("www","")
        domain = domain.replace(".","")

        rand_str = ''.join(random.sample(string.ascii_letters + string.digits,30))

        #if len(domain) >= 2:
        #    self.other_for_rss["rss_link"] = rss_link_prefix +\
        #                                     domain[-2] + rand_str + ".rss"
        #else:
        self.other_for_rss["rss_link"] = rss_link_prefix + domain + rand_str + ".rss"


    async def start(self):
        http_body = await self.get_http_body(self.site_url)
    #def start(self):
    #    http_body = self.get_http_body(self.site_url)
        if self.status["status_http_body"] == self.do_success:
            self.entry_and_link = await self.get_entry_and_link(http_body,
                                                      self.entry_css,
                                                      self.entry_link_css,
                                                      self.add_base_url,
                                                      self.base_url)
            await self.get_other(http_body,self.rss_link_prefix,
                       self.site_url,self.site_title_css,self.site_motto_css)
            if self.status["status_entry"] != self.do_success \
                or self.status["status_entry_link"] != self.do_success \
                or self.status["status_entry_and_entry_link"] != self.do_success:
                self.all_status = self.do_not_success

