import config
from selectsql import SelectSql

class RssSql(object):
    def __init__(self):
        self.database = config.get_database_config()
        self.select_sql = SelectSql(self.database)
        self.do_not_success = "do_not_success"
        self.do_success = "do_success"
        self.user = {}
        self.xpath = {}
        self.xpath_id = -1

    #not success,return []
    async def get_user_id_password(self,user_name):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetchrow("""
            SELECT user_id,user_name,password FROM rss_user WHERE user_name = $1
        """,user_name)
        await conn.close()
        return res

    #not success,return []
    async def insert_xpath(self,user_id,
                     site_url,
                     entry_css,
                     entry_link_css,
                     add_base_url,
                     rss_link_prefix,
                     site_title_css,
                     site_motto_css,
                     entry_content_css,
                     author_css,
                     datetime_css,
                     interval_time,
                     rss_link,
                     base_url):

        conn = await self.select_sql.sql_conn()
        res = await conn.fetchrow("""
                INSERT INTO xpath (user_id,site_url,
                entry_css,entry_link_css,add_base_url,
                rss_link_prefix,site_title_css,site_motto_css,
                entry_content_css,author_css,datetime_css,
                interval_time,rss_link,base_url)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
                RETURNING xpath_id;
        """,user_id,site_url,entry_css,entry_link_css,
                 add_base_url,rss_link_prefix,
                 site_title_css,site_motto_css,entry_content_css,
                 author_css,datetime_css,interval_time,rss_link,base_url)
        await conn.close()
        return res

    #not success,return []
    async def get_xpath_interval_one(self,xpath_id):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetchrow("""
        SELECT xpath_id,interval_time FROM xpath WHERE xpath_id = $1
        """,xpath_id)
        await conn.close()

        return  res

    #not success,return []
    async def get_xpath_id_interval_all(self):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetch("""
               SELECT xpath_id,interval_time FROM xpath
               """)
        await conn.close()

        return res



    #not success,return []
    async def get_xpath_from_user_id(self,user_id):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetch("""
            SELECT * FROM xpath WHERE user_id = $1
                      """, user_id)
        await conn.close()

        return res


    #not success,return []
    async def get_xpath_one_from_xpath_id(self,xpath_id):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetchrow("""
                SELECT * FROM xpath WHERE xpath_id = $1 
                             """, xpath_id)
        await conn.close()

        return res

    #not success,return []
    async def get_xpath_one_from_url_name(self,url_name):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetch("""
                SELECT * FROM xpath WHERE rss_link = $1
                      """, url_name)
        await conn.close()
        #print(f"the user_id is:{user_id}")
        #print(f"the rss is:{res}")

        return res

    #not success,return []
    async def update_xpath_one_from_rss_link(self,
                                             site_url,
                                             entry_css,
                                             entry_link_css,
                                             add_base_url,
                                             site_title_css,
                                             site_motto_css,
                                             entry_content_css,
                                             author_css,
                                             datetime_css,
                                             interval_time,
                                             rss_link,
                                             base_url
                                             ):

        conn = await self.select_sql.sql_conn()
        res = await conn.fetchrow("""
                UPDATE xpath SET site_url = $1,
                entry_css = $2,entry_link_css = $3,add_base_url = $4,
                site_title_css = $5,site_motto_css = $6,entry_content_css = $7,
                author_css = $8,datetime_css = $9,interval_time = $10,
                base_url = $11
                WHERE  rss_link = $12  RETURNING xpath_id     
               """,site_url,entry_css,entry_link_css,add_base_url,
                   site_title_css,site_motto_css,entry_content_css,
                   author_css,datetime_css,interval_time,base_url,
                   rss_link)

        await conn.close()
        return res


    #not success,return []
    async def insert_rss(self,user_id,xpath_id,site_title,rss_url_name,
                   rss_content,rss_last_build_time,rss_sha256sum):

        conn = await self.select_sql.sql_conn()
        res = await conn.fetchrow("""
                INSERT INTO rss (user_id,xpath_id,site_title,rss_url_name,
                rss_content,rss_last_build_time,rss_sha256sum)
                VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING xpath_id
               """, user_id,
                 xpath_id,
                 site_title,
                 rss_url_name,
                 rss_content,
                 rss_last_build_time,
                 rss_sha256sum)
        await conn.close()
        return res


    #not success,return []
    async def get_one_rss_from_userid_xpathid(self,user_id,xpath_id):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetchrow("""
                    SELECT * FROM rss WHERE user_id = $1 AND xpath_id = $2;
                                    """, user_id,xpath_id)
        await conn.close()

        return res


    #not success,return []
    async def get_all_rss_from_userid(self,user_id):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetch("""
                SELECT * FROM rss WHERE user_id = $1
                      """, user_id)
        await conn.close()
        #print(f"the user_id is:{user_id}")
        #print(f"the rss is:{res}")

        if len(res) == 0:
            res = [{"site_title": "rss_is_none","rss_url_name": "no_url"}]
        return res

    #not success,return []
    async def get_one_rss_from_url_name(self,url_name):
        conn = await self.select_sql.sql_conn()
        res = await conn.fetch("""
                SELECT * FROM rss WHERE rss_url_name = $1
                      """, url_name)
        await conn.close()
        #print(f"the user_id is:{user_id}")
        #print(f"the rss is:{res}")

        if len(res) == 0:
            res = [{"rss_content": "no rss,maybe deleted","rss_url_name": "no_url"}]
        return res

    #not success,return "do_not_success"
    async def update_one_rss_xpath_id(self,rss_content,
                       rss_sha256sum,xpath_id):

        conn = await self.select_sql.sql_conn()
        try:
            res = await conn.execute("""
                    UPDATE rss SET rss_content = $1,
                    rss_sha256sum = $2 WHERE  xpath_id = $3       
                   """,rss_content,
                     rss_sha256sum,xpath_id)

            await conn.close()
        except:
            res = self.do_not_success
            return res
        else:
            return res

    #not success,return []
    async def delete_one_rss_from_url_name(self,url_name):
        conn = await self.select_sql.sql_conn()
        res1 = await conn.fetchrow("""
                DELETE FROM  rss WHERE rss_url_name = $1 RETURNING *
                      """, url_name)
        res2 = await conn.fetchrow("""
                DELETE FROM xpath WHERE rss_link = $1 RETURNING *
                """,url_name)
        await conn.close()
        #print(f"the user_id is:{user_id}")
        #print(f"the rss is:{res}")

        if len(res1) != 0 and len(res2) != 0:
            res = self.do_success
        else:
            res = self.do_not_success
        return res





