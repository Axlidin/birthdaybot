from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=config.DB_PORT
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_birthday(self):
        sql = """
        CREATE TABLE IF NOT EXISTS birthday (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        Year INTEGER NOT NULL,
        Month INTEGER NOT NULL,
        Day INTEGER NOT NULL,
        telegram_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())
    async def add_birthday(self, full_name, Year, Month, Day, telegram_id):
        sql = ("INSERT INTO Birthday (full_name, Year, Month, Day, telegram_id) "
               "VALUES($1, $2, $3, $4, $5) returning *")
        return await self.execute(sql, full_name, Year, Month, Day, telegram_id, fetchrow=True)

    async def sent_date(self, Mont, Day):
        sql = "SELECT * FROM birthday WHERE EXTRACT(MONTH FROM Month) = %s AND EXTRACT(DAY FROM your_date_column) = %s"
        return await self.execute(sql, Mont, Day)

    async def select_all_birthday(self):
        sql = "SELECT * FROM birthday"
        return await self.execute(sql, fetch=True)

    async def select_birthday(self, **kwargs):
        sql = "SELECT * FROM birthday WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_birthday(self):
        sql = "SELECT COUNT(*) FROM birthday"
        return await self.execute(sql, fetchval=True)

    async def update_birthday_Year(self, Year, telegram_id):
        sql = "UPDATE birthday SET Year=$1 WHERE telegram_id=$2"
        return await self.execute(sql, Year, telegram_id, execute=True)

    async def delete_birthday(self):
        await self.execute("DELETE FROM birthday WHERE TRUE", execute=True)

    async def drop_birthday(self):
        await self.execute("DROP TABLE birthday", execute=True)

    async def my_birthday(self, tg_id):
        sql = "SELECT * FROM birthday WHERE telegram_id=$1 "
        return await self.execute(sql, tg_id, fetch=True)

    async def happy_Month_Day(self, Month, Day):
        sql = f"SELECT * FROM birthday WHERE Month = $1 AND Day = $2"
        return await self.execute(sql, Month, Day, fetch=True)

    async def delete_db_name(self, del_name):
        sql = "DELETE FROM birthday WHERE full_name=$1"
        return await self.execute(sql, del_name, execute=True)

    async def happy_day(self, t_month, t_day):
        sql = "SELECT * FROM birthday WHERE Month = $1 AND Day = $2"
        return await self.execute(sql, t_month, t_day, fetchval=True)


    ###first
    async def create_table_FIO_state(self):
        sql = """
        CREATE TABLE IF NOT EXISTS FIO_state (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_argsState(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_FIO_state(self, fullname, telegram_id):
        sql = "INSERT INTO FIO_state (fullname, telegram_id) VALUES($1, $2) returning *"
        return await self.execute(sql, fullname, telegram_id, fetchrow=True)

    async def select_all_FIO_state(self):
        sql = "SELECT * FROM FIO_state"
        return await self.execute(sql, fetch=True)

    async def select_FIO_state(self, **kwargs):
        sql = "SELECT * FROM FIO_state WHERE "
        sql, parameters = self.format_argsState(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_FIO_state(self):
        sql = "SELECT COUNT(*) FROM FIO_state"
        return await self.execute(sql, fetchval=True)

    async def update_user_FIO_state_username(self, fullname, telegram_id):
        sql = "UPDATE FIO_state Set fullname=$1 WHERE telegram_id=$2"
        return await self.execute(sql, fullname, telegram_id, execute=True)

    async def delete_FIO_state(self):
        await self.execute("DELETE FROM FIO_state WHERE TRUE", fetchrow=True)

    async def drop_FIO_state(self):
        await self.execute("DROP TABLE FIO_state", execute=True)

    async def my_bithday_see(self, tg_id):
        sql = "SELECT * FROM FIO_state WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetch=True)
    ##########gr birhday
    async def create_table_Gr_birthyday(self):
        sql = """
                    CREATE TABLE IF NOT EXISTS Gr_birthyday (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    Year INTEGER NOT NULL,
                    Month INTEGER NOT NULL,
                    Day INTEGER NOT NULL,
                    guruh_name VARCHAR(255) NOT NULL,
                    guruh_id BIGINT 
                    );
                    """
        await self.execute(sql, execute=True)

    async def add_Gr_birthyday(self,
                               full_name,
                               Year,
                               Month,
                               Day,
                               guruh_id,
                               guruh_name):
        sql = """
           INSERT INTO Gr_birthyday (guruh_name, 
                            full_name,
                            Year,
                            Month,
                            Day,
                             guruh_id) VALUES ($1, $2, $3, $4, $5, $6) returning *
           """
        await self.execute(sql, guruh_name,
                                            full_name,
                                            Year,
                                            Month,
                                            Day,
                                            guruh_id, fetchrow=True)

    async def select_all_Gr_birthyday(self):
        sql = """
           SELECT * FROM Gr_birthyday
           """
        return await self.execute(sql, fetch=True)

    async def select_Gr_birthyday(self, **kwargs):
        sql = "SELECT * FROM Gr_birthyday WHERE "
        ql, parameters = self.format_argsState(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_Gr_birthyday(self):
        sql = "SELECT COUNT(*) FROM Gr_birthyday"
        return await self.execute(sql, fetchval=True)

    async def delete_Gr_birthyday(self):
        await self.execute("DELETE FROM Gr_birthyday WHERE TRUE", fetchrow=True)

    async def drop_Gr_birthyday(self):
        await self.execute("DROP TABLE Gr_birthyday", execute=True)

    async def my_user_seeGR_user(self, tg_id):
        sql = "SELECT * FROM Gr_birthyday WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetch=True)

    async def my_user_seeGR_gr(self, guruh_id):
        sql = "SELECT * FROM Gr_birthyday WHERE guruh_id=$1"
        return await self.execute(sql, guruh_id, fetch=True)

    async def see_mont_day(self, month, day):
        sql = "SELECT * FROM Gr_birthyday WHERE Month=$1 AND Day=$2"
        return await self.execute(sql, month, day, fetch=True)

    async def delete_birhdaygr(self, del_name):
        sql = "DELETE FROM Gr_birthyday WHERE full_name=$1"
        return await self.execute(sql, del_name, fetch=True)

    ##########Guruhlar
    async def create_table_Guruhlar(self):
        sql = """
              CREATE TABLE IF NOT EXISTS Guruhlar  (
                    id SERIAL PRIMARY KEY,
                    chat_id BIGINT NOT NULL UNIQUE,
                    GroupName varchar(255) NOT NULL);
                                      """
        await self.execute(sql, execute=True)

    async def add_Guruhlar(self, chat_id, GroupName):
        sql = """
              INSERT INTO Guruhlar  (chat_id, GroupName) VALUES ($1, $2) returning *
              """
        return await self.execute(sql, chat_id, GroupName, fetchrow=True)

    async def select_all_Guruhlar(self):
        sql = """
              SELECT * FROM Guruhlar 
              """
        return await self.execute(sql, fetch=True)

    async def select_Guruhlar(self, **kwargs):
        sql = "SELECT * FROM Guruhlar  WHERE "
        sql, parameters = self.format_argsState(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_Guruhlar(self):
        sql = "SELECT COUNT(*) FROM Guruhlar"
        return await self.execute(sql, fetchval=True)

    async def delete_Guruhlar(self):
        await self.execute("DELETE FROM Guruhlar WHERE TRUE", fetchrow=True)

    async def drop_Guruhlar(self):
        await self.execute("DROP TABLE Guruhlar", execute=True)

    async def my_user_seeGuruhlar_user(self, chat_id):
        sql = "SELECT * FROM Guruhlar WHERE chat_id=$1"
        return await self.execute(sql, chat_id, fetch=True)

    ###################auotinfo########
    async def auto_info_user(self, month, day):
        sql = """SELECT * FROM birthday WHERE Month = $1 AND Day = $2"""
        return await self.execute(sql, month, day, fetchval=True)

    async def auto_info_gr(self, month, day):
        sql = """SELECT * FROM Gr_birthyday WHERE Month = $1 AND Day = $2"""
        return await self.execute(sql, month, day, fetch=True)