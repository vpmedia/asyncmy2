# /// script
# dependencies = [
#   "greenlet",
#   "sqlalchemy",
# ]
# ///

import asyncio
import logging
import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

engine = create_async_engine("mysql+asyncmy://user:pass@hostname/dbname?charset=utf8mb4")

logging.basicConfig(level=logging.INFO)


async def main():
    pwd = os.getenv("MYSQL_PASS", "123456")
    engine = create_async_engine(f"mysql+asyncmy://root:{pwd}@127.0.0.1/test?charset=utf8mb4")
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(result.one())


if __name__ == "__main__":
    asyncio.run(main())
