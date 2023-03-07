from multiprocessing import Pool

import aiomysql

from tgbot.config import load_config


class ExternalDatabase:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        config = load_config(".env")
        pool = await aiomysql.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            db=config.db.database
        )
        return cls(pool)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)])
        return sql, tuple(parameters.values())

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM reciklomat_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
