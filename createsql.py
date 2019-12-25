#import psycopg2
#import datetime
from selectsql import SelectSql

class CreateTable(object):
    """
    when initiate,create all table in postgresql
    """
    def __init__(self,database):
        self.database = database
        #self.user = user_table
        #self.xpath = xpath_table
        #self.rss = rss_table

    async def create_user_table(self):
        select_sql = SelectSql(self.database)
        conn = await select_sql.sql_conn()

        res = await conn.execute("""
                CREATE TABLE rss_user(
                user_id serial PRIMARY KEY,
                user_name varchar NOT NULL DEFAULT 'guest',
                email varchar NOT NULL ,
                password varchar NOT NULL,phone varchar,
                paid numeric,cash numeric,priviage varchar,
                verified bool NOT NULL DEFAULT TRUE,
                created_date timestamp NOT NULL ,
                last_login timestamp NOT NULL
                );
        """)
        await conn.close()

        return res


    async def create_xpath_table(self):
        select_sql = SelectSql(self.database)
        conn = await select_sql.sql_conn()

        res = await conn.execute("""
                    CREATE TABLE xpath(
                    xpath_id serial PRIMARY KEY,
                    user_id integer REFERENCES rss_user(user_id),
                    site_url varchar NOT NULL,
                    entry_css varchar NOT NULL,
                    entry_link_css varchar NOT NULL,
                    add_base_url bool NOT NULL,
                    rss_link_prefix varchar NOT NULL,
                    site_title_css varchar NOT NULL,
                    site_motto_css varchar NOT NULL,
                    entry_content_css varchar NOT NULL,
                    author_css varchar NOT NULL,
                    datetime_css varchar NOT NULL,
                    interval_time bigint NOT NULL DEFAULT 30
                    );
        """)
        await conn.close()

        return res

    async def creat_rss_table(self):
        select_sql = SelectSql(self.database)
        conn = await select_sql.sql_conn()

        res = await conn.execute("""
                    CREATE TABLE rss(
                    user_id integer REFERENCES rss_user(user_id),
                    xpath_id integer REFERENCES xpath(xpath_id),
                    site_title varchar NOT NULL,
                    rss_url_name varchar NOT NULL,
                    rss_content varchar NOT NULL,
                    rss_last_build_time varchar NOT NULL,
                    rss_sha256sum varchar NOT NULL
                    );
        """)
        await conn.close()

        return res



