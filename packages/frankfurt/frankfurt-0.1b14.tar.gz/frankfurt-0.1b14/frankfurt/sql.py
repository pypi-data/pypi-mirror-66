import logging

import asyncpg

from typing import Dict, Optional, List, Any, Union, Type
from dataclasses import dataclass, field

from .models import BaseModel


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class StatementContext:
    values : List[Any] = field(default_factory=list)


class Statement:
    def __stmt__(self, ctx : StatementContext):
        return str(self)


@dataclass
class ColumnConstraintReference:
    reftable: str
    refcolumn: Optional[str] = None
    on_delete: Optional[str] = None
    on_update: Optional[str] = None

    def __str__(self):
        stmt = f'REFERENCES "{self.reftable}"'

        if self.refcolumn:
            stmt = f'{stmt} ("{self.refcolumn}")'

        if self.on_delete:
            stmt = f'{stmt} ON DELETE {self.on_delete}'

        return stmt


@dataclass
class ColumnConstraint:
    not_null: bool = False
    primary_key: bool = False
    references: Optional[ColumnConstraintReference] = None
    unique : bool = False

    def __bool__(self):

        if self.not_null:
            return True

        if self.primary_key:
            return True

        if self.references:
            return True

        if self.unique:
            return True

        return False

    def __str__(self):

        constraints = []

        if self.not_null:
            constraints.append("NOT NULL")

        if self.unique:
            constraints.append("UNIQUE")

        if self.primary_key:
            constraints.append("PRIMARY KEY")

        if self.references:
            constraints.append(str(self.references))

        return " ".join(constraints)


@dataclass
class Column:

    name : str
    data_type : str
    constraint : Optional[ColumnConstraint] = None

    def __init__(
            self,
            name : str,
            data_type : str,
            constraint : Optional[ColumnConstraint] = None
    ):

        self.name = name
        self.data_type = data_type
        self.constraint = constraint

    def __str__(self):
        stmt = f'"{self.name}" {self.data_type}'

        if self.constraint:
            stmt = f"{stmt} {self.constraint}"
        return stmt


@dataclass
class WhereClause(Statement):
    def __bool__(self):
        return False

    def __and__(self, other):

        if isinstance(other, dict):
            parts = []
            for n, v in other.items():
                lhs = ExpressionColumnName(n)
                rhs = ExpressionLiteralValue(v)
                parts.append(WhereClauseEquality(lhs=lhs, rhs=rhs))
            return WhereClauseAnd(parts=parts)

        if isinstance(other, WhereClauseAnd):
            return WhereClauseAnd(parts=other.parts)

        if isinstance(other, WhereClause):
            return WhereClauseAnd(parts=[other])

        raise NotImplementedError("Operation not implemented")


class Expression(Statement):
    def __bool__(self):
        return False


@dataclass
class WhereClauseEquality(WhereClause):
    lhs: Union[Expression, str]
    rhs: Union[Expression, str]

    def __bool__(self):
        return True

    def __stmt__(self, ctx):
        return f'{self.lhs.__stmt__(ctx)}={self.rhs.__stmt__(ctx)}'


@dataclass
class WhereClauseAnd(WhereClause):
    parts: List[WhereClause] = field(default_factory=list)

    def __bool__(self):
        return len(self.parts) > 0

    def __str__(self):
        return " AND ".join(f'({_})' for _ in self.parts)

    def __stmt__(self, ctx):
        return " AND ".join(f'{_.__stmt__(ctx)}' for _ in self.parts)

    def __and__(self, other):
        if isinstance(other, WhereClauseAnd):
            return WhereClauseAnd(parts=self.parts + other.parts)

        if isinstance(other, WhereClause):
            return WhereClauseAnd(parts=self.parts + [other])

        if isinstance(other, dict):
            return self & (WhereClause() & other)

        raise NotImplementedError("Operation not implemented")


@dataclass
class ExpressionColumnName(Expression):
    name : str

    def __bool__(self):
        return self.name != ""

    def __str__(self):
        return f'"{self.name}"'


@dataclass
class ExpressionLiteralValue(Expression):
    value : Any

    def __bool__(self):
        return str(self.value) != ""

    def __stmt__(self, context):
        context.values.append(self.value)
        i = len(context.values)
        return f'${i}'


class Asterisk(Expression):
    def __bool__(self):
        return True

    def __str__(self):
        return '*'


class WhereClauseMixin:

    _where : WhereClause

    def where(self, *args, **kwargs):

        # When args are passed are considered to be where clauses.
        for arg in args:
            self._where &= arg

        for name, value in kwargs.items():
            lhs = ExpressionColumnName(name=name)
            rhs = ExpressionLiteralValue(value=value)
            self._where &= WhereClauseEquality(lhs=lhs, rhs=rhs)

            return self


class ReturningMixin:

    _returning : List[str]

    def returning(self, *fields):
        for name in fields:
            self._returning.append(name)

        return self


class PartialBase:
    _conn : Optional[asyncpg.Connection] = None

    def conn(self, conn):
        self._conn = conn

        return self


@dataclass
class SetClause(Statement):
    values : Dict[str, Any] = field(default_factory=dict)

    def __stmt__(self, ctx):
        set_values = []
        for name, value in self.values.items():
            ctx.values.append(value)
            set_values.append(f'"{name}"=${len(ctx.values)}')

        return ' '.join(set_values)


class PartialUpdate(WhereClauseMixin, ReturningMixin, PartialBase):

    _values : Dict[str, Any]
    _model : Type[BaseModel]

    def __init__(self, table_name : str, conn=None, db=None):
        self._table_name = table_name
        self._where = WhereClause()
        self._conn = conn
        self._set_clause = SetClause()
        self._returning = []

    def values(self, **kwargs):
        for name, value in kwargs.items():
            self._set_clause.values[name] = value

        return self

    def __await__(self):

        # Start with a statement context.
        ctx = StatementContext()

        stmt = f'UPDATE "{self._table_name}"'

        # Append a set clause.
        if self._set_clause:
            stmt = f'{stmt} SET {self._set_clause.__stmt__(ctx)}'

        # Append a where clause.
        if self._where:
            stmt = f'{stmt} WHERE {self._where.__stmt__(ctx)}'

        # Append the returning columns.
        if self._returning:
            returning = ', '.join(f'"{name}"' for name in self._returning)
            stmt = f"{stmt} RETURNING ({returning})"

        # Log the statement.
        logger.debug(stmt)

        # Wait for the update.
        return self._conn.fetchrow(stmt, *ctx.values).__await__()


class PartialSelect(WhereClauseMixin, PartialBase):

    def __init__(self, model, conn=None):
        self._conn = conn
        self._model = model
        self._where = WhereClause()

    async def one(self, conn=None):
        #: Return one instance of a model or raise an error.

        if conn is None:
            conn = self.conn

        #: Select all the fields.
        select = list(self._model._meta.fields.keys())
        select = [ExpressionColumnName(name=name) for name in select]

        # Table name to select from.
        from_table = self._model._meta.table_name

        # Create the statement.
        stmt = Select(
            select=select,
            where=self._where,
            from_items=[f'"{from_table}"']
        )

        # TODO: Add a count statement first and then a fetch.
        # Get a list of records.
        records = await stmt.fetch(conn=conn)

        if len(records) != 1:
            raise Exception("Return only one element.")

        # TODO: This should
        return self._model.from_record(records[0])


@dataclass
class Update(Statement):
    pass


@dataclass
class Select(Statement):
    """ Select statement. """

    select: Union[Asterisk, List[Expression], List[str]]
    where: WhereClause
    from_items: List[Any]

    async def fetch(self, conn):

        ctx = StatementContext()

        stmt = "SELECT"

        if self.select:
            if isinstance(self.select, list):
                select = ', '.join(str(_) for _ in self.select)
            else:
                select = self.select

            stmt = f"SELECT {select}"

        if self.from_items:
            from_items = ", ".join(str(item) for item in self.from_items)
            stmt = f"{stmt} FROM {from_items}"

        if self.where:
            stmt = f"{stmt} WHERE {self.where.__stmt__(ctx)}"

        logger.debug(stmt)
        return await conn.fetch(stmt, *ctx.values)


class Insert(Statement):
    """ Insert statement. """

    table_name : str
    values : Dict[str, Any]
    returning: List[str]

    def __init__(
            self, table_name : str,
            values : Optional[Dict[str, Any]] = None,
            returning : Optional[List[str]] = None
    ):

        self.table_name = table_name
        self.values = values if values is not None else {}
        self.returning = returning if returning is not None else []

    async def fetchrow(self, conn):

        stmt = f'INSERT INTO "{self.table_name}"'

        values = []

        if self.values:
            cols = []
            placeholders = []

            for i, (name, value) in enumerate(self.values.items()):
                cols.append(f'"{name}"')
                placeholders.append(f'${i + 1}')
                values.append(value)

            cols = ', '.join(cols)
            placeholders = ', '.join(placeholders)
            stmt = f"{stmt} ({cols}) VALUES ({placeholders})"

        if self.returning:
            returning = ', '.join(f'"{name}"' for name in self.returning)
            stmt = f"{stmt} RETURNING ({returning})"

        logger.debug(stmt)
        return await conn.fetchrow(stmt, *values)


class CreateTable(Statement):

    name : str
    columns : List[Column]

    def __init__(self, name : str, columns : List[Column]):
        self.name = name
        self.columns = columns

    async def execute(self, conn):
        stmt = f'CREATE TABLE IF NOT EXISTS "{self.name}"'

        if self.columns:
            columns = ', '.join(str(col) for col in self.columns)
            stmt = f"{stmt} ({columns})"

        logger.debug(stmt)
        return await conn.execute(stmt)
