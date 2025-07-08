import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import settings
from app.db.db import Base
from app.db.models import *

# Alembic Config object
config = context.config

# Загружаем конфиг логгирования
fileConfig(config.config_file_name)

# Устанавливаем URL подключения из settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Метадата для автогенерации
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection):
        def run_migrations_in_sync(sync_connection):
            context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
            context.run_migrations()

        await connection.run_sync(run_migrations_in_sync)

    asyncio.run(_run(connectable, do_run_migrations))


async def _run(connectable, do_migrations):
    async with connectable.connect() as connection:
        await do_migrations(connection)




if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
