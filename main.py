from tornado.web import RequestHandler, HTTPError
import tornado.web
import tornado.gen
from tornado import escape
import hashlib
from rsssql import RssSql
import config
from timerevent import TimerEvent
from entrylink import EntryLink
from rssbody import RssBody
from rssfeed import RssFeed
import datetime
import  tornado.ioloop
import asyncio

home_uri = ""
absolute_uri_prefix = ""
refresh_interval = 0

class HomeHandler(RequestHandler):
    async def get(self):
        user_id = self.get_secure_cookie("user_id")
        if  not user_id:
            self.redirect(self.reverse_url("login"))
            return

        rss_sql = RssSql()
        rss = await rss_sql.get_all_rss_from_userid(int(user_id))

        await self.render("home.html",rss = rss,
                          request_uri = home_uri)

    async def post(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            self.redirect(self.reverse_url("login"))
            return

        rss_sql = RssSql()
        rss = await rss_sql.get_all_rss_from_userid(int(user_id))

        await self.render("home.html",rss = rss,
                          request_uri = home_uri)


class LoginHandler(RequestHandler):
    async def get(self):
        incorrect = self.get_secure_cookie("incorrect") or 0
        if int(incorrect) > 10:
            await self.render("block.html")
            return

        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            temp_uri = home_uri + "login"
            await self.render("login.html",request_uri = temp_uri,
                              incorrect_times = incorrect)
            return


    async def post(self):
        incorrect = self.get_secure_cookie("incorrect") or 0
        if int(incorrect) > 10:
            await self.render("block.html")
            return

        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            user_name = escape.xhtml_escape(self.get_body_argument("user_name"))
            password = escape.xhtml_escape(self.get_body_argument("password"))

            sha256 = hashlib.sha256()
            sha256.update(password.encode('utf-8'))
            res_password = sha256.hexdigest()

            rss_sql = RssSql()
            user_id_name_passwd = await  rss_sql.get_user_id_password(user_name)

            if not user_id_name_passwd:
                incorrect = int(incorrect) + 1
                #0.01 means 0.01 day,14minutes later will reset?
                self.set_secure_cookie("incorrect", str(incorrect),0.01)

                temp_uri = home_uri + "login"
                await self.render("login.html", request_uri=temp_uri,
                                  incorrect_times=incorrect)
                return

            else:
                if res_password == user_id_name_passwd["password"]:
                    # use user_id as cookie
                    self.set_secure_cookie("user_id",
                                           str(user_id_name_passwd["user_id"]))
                    self.redirect(self.reverse_url("home"))
                    return
                else:
                    incorrect = int(incorrect) + 1
                    self.set_secure_cookie("incorrect", str(incorrect),0.01)

                    temp_uri = home_uri + "login"
                    await self.render("login.html", request_uri=temp_uri,
                                      incorrect_times=incorrect)
                    return



class LogoutHandler(RequestHandler):
    async def get(self):
        self.clear_cookie("user_id")
        self.redirect(self.reverse_url("login"))
        return


class AddrssHandler(RequestHandler):
    async def get(self):
        print(f"come here?")
        user_id = self.get_secure_cookie("user_id")
        if  not user_id:
            self.redirect(self.reverse_url("login"))
            return

        await self.render("addrss.html",home_uri = home_uri,
                          request_uri = home_uri + "add_rss")

    async def post(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            self.redirect(self.reverse_url("login"))
            return

        site_url = escape.xhtml_escape(self.get_body_argument("site_url"))
        entry_css = self.get_body_argument("entry_css")
        entry_link_css = self.get_body_argument("entry_link_css")
        add_base_url = escape.xhtml_escape(self.get_body_argument("add_base_url"))
        site_title_css = self.get_body_argument("site_title_css")
        site_motto_css = self.get_body_argument("site_motto_css")
        entry_content_css = self.get_body_argument("entry_content_css")
        author_css = self.get_body_argument("author_css")
        datetime_css = self.get_body_argument("datetime_css")
        base_url = self.get_body_argument("base_url")
        #print(f"the entry_content_css is:{self.get_body_argument('entry_content_css')}")

        #xpath css can not contain space " "
        site_url = site_url.replace(" ","")
        entry_css = entry_css.replace(" ","")
        entry_link_css = entry_link_css.replace(" ","")
        add_base_url = add_base_url.replace(" ","")
        site_title_css = site_title_css.replace(" ","")
        site_motto_css = site_motto_css.replace(" ","")
        entry_content_css = entry_content_css.replace(" ","")
        author_css = author_css.replace(" ","")
        datetime_css = datetime_css.replace(" ","")
        base_url = base_url.replace(" ","")


        if self.get_arguments('dry_run_list'):
            save_button = "dry_run_list"
        elif self.get_arguments('save'):
            save_button = "save"
        else:
            save_button = "dry_run_content"

        if str.lower(add_base_url) == "true":
            add_base_url = True
        else:
            add_base_url = False


        entry_link = EntryLink(site_url,entry_css,
                               entry_link_css,add_base_url,
                               absolute_uri_prefix,
                               site_title_css,
                               site_motto_css,base_url)
        try:
            await entry_link.start()
        except:
            pass

        if entry_link.all_status != entry_link.do_success:
            await self.render("error.html",request_uri = home_uri,
                        error_msg = entry_link.status)
            return



        if save_button == "dry_run_list":
            await self.render("entry_list.html",
                              entry_list = entry_link.entry_and_link,
                              request_uri = home_uri)
            return



        rss_body = RssBody(entry_link.entry_and_link,
                           entry_content_css,author_css,
                           datetime_css)
        try:
            await rss_body.start()
        except:
            pass
        if rss_body.all_status != rss_body.do_success:
            await self.render("error.html", request_uri=home_uri,
                              error_msg=rss_body.status)
            return

        rss_feed = RssFeed(rss_body.rss_body,entry_link)
        try:
            await rss_feed.start()
        except:
            pass

        rss_sql = RssSql()
        res_xpath = await rss_sql.insert_xpath(int(user_id),site_url,
                                   entry_css,entry_link_css,
                                   add_base_url,absolute_uri_prefix,
                                   site_title_css,site_motto_css,
                                   entry_content_css,author_css,
                                   datetime_css,refresh_interval,
                                   entry_link.other_for_rss["rss_link"],
                                   base_url)
        xpath_id = res_xpath["xpath_id"]

        sha256 = hashlib.sha256()
        sha256.update(rss_feed.rss_xml.encode('utf-8'))
        res_rss = sha256.hexdigest()


        last_build_time = datetime.datetime.now().strftime("%Y-%m-%d")
        await rss_sql.insert_rss(int(user_id),xpath_id,
                                 entry_link.other_for_rss["site_title"],
                                 entry_link.other_for_rss["rss_link"],
                                 #escape.xhtml_unescape(rss_feed.rss_xml),
                                 rss_feed.rss_xml,
                                 last_build_time,
                                 res_rss)

        self.redirect(self.reverse_url("home"))



class RssHandler(RequestHandler):
    async def get(self):
        req_uri = self.request.uri
        req_uri = req_uri.split("/")
        rss_url_name = absolute_uri_prefix + req_uri[-1]

        rss_sql = RssSql()
        rss = await rss_sql.get_one_rss_from_url_name(rss_url_name)
        #self.set_header("Content-Type", "application/atom+xml")
        await self.render("feed.xml",rss_content = rss[0]["rss_content"])
        #self.write(rss[0]["rss_content"])

    async def post(self):
        req_uri = self.request.uri
        req_uri = req_uri.split("/")
        rss_url_name = absolute_uri_prefix + req_uri[-1]

        rss_sql = RssSql()
        rss = await rss_sql.get_one_rss_from_url_name(rss_url_name)
        #self.set_header("Content-Type", "application/atom+xml")
        await self.render("feed.xml", rss_content=rss[0]["rss_content"])
        #self.write(rss[0]["rss_content"])

class PrivaterssHandler(RequestHandler):
    async def get(self):
        user_id = self.get_secure_cookie("user_id")
        if  not user_id:
            self.redirect(self.reverse_url("login"))
            return

        rss_sql = RssSql()
        rss = await rss_sql.get_all_rss_from_userid(int(user_id))

        self.set_header("Content-Type", "application/atom+xml")
        self.write(rss[0]["rss_content"])

    async def post(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            self.redirect(self.reverse_url("login"))
            return

        rss_sql = RssSql()
        rss = await rss_sql.get_all_rss_from_userid(int(user_id))
        self.set_header("Content-Type", "application/atom+xml")
        self.write(rss[0]["rss_content"])

class DeleterssHandler(RequestHandler):
    async def post(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            self.redirect(self.reverse_url("login"))
            return

        url_name = escape.xhtml_escape(self.get_body_argument("url_name"))
        #print(f"the url_name is{url_name}")

        rss_sql = RssSql()
        res = await rss_sql.delete_one_rss_from_url_name(url_name)
        self.write(res)

class EditrssHandler(RequestHandler):
    async def post(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            self.redirect(self.reverse_url("login"))
            return

        url_name = escape.xhtml_escape(self.get_body_argument("url_name"))

        rss_sql = RssSql()
        rss = await rss_sql.get_xpath_one_from_url_name(url_name)

        await self.render("edit.html", rss=rss,
                request_uri=home_uri)
        return


class UpdaterssHandler(RequestHandler):
    async def post(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id:
            self.redirect(self.reverse_url("login"))
            return

        site_url = self.get_body_argument("site_url")
        entry_css = self.get_body_argument("entry_css")
        entry_link_css = self.get_body_argument("entry_link_css")
        add_base_url = self.get_body_argument("add_base_url")
        site_title_css = self.get_body_argument("site_title_css")
        site_motto_css = self.get_body_argument("site_motto_css")
        entry_content_css = self.get_body_argument("entry_content_css")
        author_css = self.get_body_argument("author_css")
        datetime_css = self.get_body_argument("datetime_css")
        interval_time = float(self.get_body_argument("interval_time")) * 60 * 60
        interval_time = int(interval_time)
        rss_link = escape.xhtml_escape(self.get_body_argument("rss_link"))
        base_url = self.get_body_argument("base_url")

        if str.lower(add_base_url) == "true":
            add_base_url = True
        else:
            add_base_url = False

        rss_sql = RssSql()
        res = await rss_sql.update_xpath_one_from_rss_link(site_url,entry_css,
                                                     entry_link_css,add_base_url,
                                                     site_title_css,site_motto_css,entry_content_css,
                                                     author_css,datetime_css,interval_time,
                                                     rss_link,base_url)
        await self.render("update_status.html",res = int(res["xpath_id"]),request_uri = home_uri)



class Application(tornado.web.Application):
    def __init__(self,home_uri,settings):
        tornado.web.Application.__init__(self, [
            tornado.web.url(f'{home_uri}?', HomeHandler,
                            name="home"),
            tornado.web.url(f'{home_uri}login', LoginHandler,
                            name="login"),
            tornado.web.url(f'{home_uri}logout', LogoutHandler,
                            name="logout"),
            tornado.web.url(f'{home_uri}add_rss', AddrssHandler,
                            name="add_rss"),
            tornado.web.url(f'{home_uri}.*\.rss', RssHandler,
                            name="get_rss"),
            tornado.web.url(f'{home_uri}private_rss', PrivaterssHandler,
                            name="private_rss"),
            tornado.web.url(f'{home_uri}delete_rss', DeleterssHandler,
                            name="delete_rss"),
            tornado.web.url(f'{home_uri}edit_rss', EditrssHandler,
                            name="edit_rss"),
            tornado.web.url(f'{home_uri}update_rss', UpdaterssHandler,
                            name="update_rss"),
        ], **settings)



if __name__ == "__main__":

    settings = config.get_app_config()
    other_configs = config.get_other_config()
    home_uri = other_configs["home_uri"]
    listen_port = other_configs["listen_port"]
    absolute_uri_prefix = other_configs["absolute_uri_prefix"]
    rss_site_uri = other_configs["rss_site_uri"]
    refresh_interval = other_configs["refresh_interval"] * 60


    app = Application(home_uri,settings)
    app.listen(listen_port)

    timer_event = TimerEvent(refresh_interval)

    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.add_callback(timer_event.timer_execute)


    io_loop.start()
