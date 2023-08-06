import pytest
from mock import AsyncMock, MagicMock, call, patch


@pytest.mark.asyncio
@patch('frankfurt.database.asyncpg.create_pool', new=AsyncMock())
async def test_conn():
    from frankfurt import Database, fields

    db = Database()

    class Example(db.Model):
        text = fields.CharField(max_length=200)

    assert db._conn.get() is None

    db.pool = MagicMock

    await db.create_pool('__url__')

    conn = await db.acquire()

    conn.transaction = MagicMock()

    assert db._conn.get() is not None

    await db.create_all_tables()

    await db.release()

    assert db._conn.get() is None

    conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "example" ("text" VARCHAR(200))'
    )
