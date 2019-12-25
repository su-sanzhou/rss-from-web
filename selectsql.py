import asyncpg

class SelectSql(object):
    def __init__(self,database):
        self.dbname = database.get("dbname")
        self.dbuser = database.get("user")
        self.dbpasswd = database.get("password")
        self.dbhost = database.get("host")
        self.dbport = database.get("port")

    async def sql_conn(self):
        try:
            conn = await asyncpg.connect(database = self.dbname,
                                    user = self.dbuser,
                                    password = self.dbpasswd,
                                    host = self.dbhost,
                                    port = self.dbport
                                    )
        except:
            print("I am unable to connect to the database.")
            await conn.close()
            return {"conn","wrong_conn"}
        else:
            return conn


