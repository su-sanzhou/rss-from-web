import datetime
import hashlib
import config
import psycopg2

def syncpg_connect(database):
    database = config.get_database_config()
    try:
        conn = psycopg2.connect(dbname = database["dbname"],
                                user = database["user"],
                                password = database["password"],
                                host = database["host"])
    except:
        print("can not connect to database using psycopg2")
        print(f"the conn is {conn}")
    else:
        cur = conn.cursor()
    return conn,cur

def syncpg_create_user_table(cur):
    try:
        res = cur.execute("""
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
    except:
        print("can not create db rss_user using psycopg2")
    else:
        print(f"create rss_user table success")


def syncpg_create_xpath_table( cur):
    try:
        res = cur.execute("""
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
                    interval_time bigint NOT NULL DEFAULT 30,
                    rss_link varchar NOT NULL,
                    base_url varchar NOT NULL
                    );
        """)
    except:
        print("can not create db xpath using psycopg2")
    else:
        print(f"create table xpath success")

def syncpg_create_rss_table( cur):
    try:
        res = cur.execute("""
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
    except:
        print("can not create db rss using psycopg2")
    else:
        print("create table rss success")

def syncopg_insert_admin_user(cur):

    passwd = "password"
    sha256 = hashlib.sha256()
    sha256.update(passwd.encode('utf-8'))
    passwd_sha = sha256.hexdigest()

    try:
        res =  cur.execute("""
            INSERT INTO rss_user (user_name,email,
            password,phone,paid,cash,priviage,
            verified,created_date,last_login) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
           """,("admin","admin@test.com",passwd_sha,
             "13810000000",0.0,0.0,"administrator",
             False,datetime.datetime.now(),
             datetime.datetime.now()))
    except:
        print("there some wong when insert admin")
    else:
        print("init admin user success")




if __name__ == "__main__":
    database = config.get_database_config()
    conn,cur = syncpg_connect(database)
    syncpg_create_user_table(cur)
    conn.commit()
    syncpg_create_xpath_table(cur)
    conn.commit()
    syncpg_create_rss_table(cur)
    conn.commit()
    syncopg_insert_admin_user(cur)
    conn.commit()

    cur.close()
    conn.close()


