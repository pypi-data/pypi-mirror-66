import pytest
from mock import AsyncMock


@pytest.mark.asyncio
async def test_create_table_no_columns():
    import frankfurt.sql

    conn = AsyncMock()

    await frankfurt.sql.PartialCreateTable(conn, 'test', {})

    conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "test"'
    )


@pytest.mark.asyncio
async def test_create_table_with_many_columns():
    import frankfurt.sql

    conn = AsyncMock()

    columns = {
        'col_0': frankfurt.sql.ColumnClause('dt_0'),
        'col_1': frankfurt.sql.ColumnClause('dt_1')
    }

    await frankfurt.sql.PartialCreateTable(conn, 'test').columns(**columns)

    conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "test" ("col_0" dt_0, "col_1" dt_1)'
    )


@pytest.mark.asyncio
async def test_simple_insert():
    import frankfurt.sql

    conn = AsyncMock()
    conn.fetchrow.return_value = {'a' : 1, 'b': 2}

    ins = frankfurt.sql.PartialInsert(conn, 'test')
    ins.values(a=1)
    ins.returning('a', 'b')

    record = await ins

    assert record['a'] == 1
    assert record['b'] == 2

    conn.fetchrow.assert_called_with(
        'INSERT INTO "test" ("a") VALUES ($1) RETURNING ("a", "b")', 1
    )


@pytest.mark.asyncio
async def test_delete_full_table():
    import frankfurt.sql

    conn = AsyncMock()

    # Define.
    delete = frankfurt.sql.PartialDelete(conn, "table")

    # Execute on await.
    await delete

    conn.fetch.assert_awaited_once_with(
        'DELETE FROM "table"'
    )


@pytest.mark.asyncio
async def test_delete_where():
    import frankfurt.sql

    conn = AsyncMock()

    # Define.
    delete = frankfurt.sql.PartialDelete(conn, "table")
    delete.where(pk=1, text="hola")

    # Execute on await.
    await delete

    # Assert for where values.
    conn.fetch.assert_awaited_once_with(
        'DELETE FROM "table" WHERE "pk"=$1 AND "text"=$2', 1, 'hola'
    )
