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


@dataclass
class SetClause(Statement):
    values : Dict[str, Any] = field(default_factory=dict)

    def __bool__(self):
        return len(self.values) > 0

    def __stmt__(self, ctx):
        set_values = []
        for name, value in self.values.items():
            ctx.values.append(value)
            set_values.append(f'"{name}"=${len(ctx.values)}')

        return ', '.join(set_values)


@dataclass
class ReturningClause(Statement):
    names : List[str] = field(default_factory=list)

    def __bool__(self):
        return len(self.names) > 0

    def __stmt__(self, ctx):
        return ', '.join(f'"{name}"' for name in self.names)


@dataclass
class SelectClause(Statement):
    names : List[str] = field(default_factory=list)

    def __bool__(self):
        return len(self.names) > 0

    def __stmt__(self, ctx):
        return ', '.join(f'"{name}"' for name in self.names)


@dataclass
class ValuesClause(Statement):
    values : Dict[str, Any] = field(default_factory=dict)

    def __bool__(self):
        return len(self.values) > 0

    def __stmt__(self, ctx):

        cols = []
        placeholders = []

        for name, value in self.values.items():
            ctx.values.append(value)
            cols.append(f'"{name}"')
            placeholders.append(f'${len(ctx.values)}')

        return f'({", ".join(cols)}) VALUES ({", ".join(placeholders)})'


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

    _returning : ReturningClause

    def returning(self, *names):
        self._returning.names.extend(names)
        return self


class SelectMixin:
    _select : SelectClause

    def select(self, *names):
        self._select.names.extend(names)
        return self


class ValuesMixin:
    _values : ValuesClause

    def values(self, **kwargs):
        self._values.values.update(kwargs)
        return self


class PartialBase:
    _conn : Optional[asyncpg.Connection] = None

    def conn(self, conn):
        self._conn = conn

        return self


class PartialDelete(WhereClauseMixin, ReturningMixin, PartialBase):

    def __init__(self, table_name : str, conn=None, mapper=None):
        self._table_name = table_name
        self._conn = conn
        self._where = WhereClause()
        self._returning = ReturningClause()

    def __await__(self):

        # Start with a statement context.
        ctx = StatementContext()

        stmt = f'DELETE FROM "{self._table_name}"'

        # Append a where clause (Mmm, en error here could
        # delete a whole table.)
        if self._where:
            stmt = f'{stmt} WHERE {self._where.__stmt__(ctx)}'

        # Append the returning columns.
        if self._returning:
            stmt = f"{stmt} RETURNING ({self._returning.__stmt__(ctx)})"

        return self._conn.fetch(stmt, *ctx.values).__await__()


class PartialUpdate(WhereClauseMixin, ReturningMixin, PartialBase):

    _values : Dict[str, Any]

    def __init__(self, table_name : str, conn=None, mapper=None):
        self._table_name = table_name
        self._where = WhereClause()
        self._conn = conn
        self._set_clause = SetClause()
        self._returning = ReturningClause()
        self._mapper = mapper

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
            stmt = f"{stmt} RETURNING ({self._returning.__stmt__(ctx)})"

        # Log the statement.
        logger.debug(stmt)

        # Wait for the update.
        result = (yield from self._conn.fetchrow(stmt, *ctx.values).__await__())

        if callable(self._mapper):
            return self._mapper(result)

        return result


class PartialSelect(WhereClauseMixin, SelectMixin, PartialBase):
    _mapper : Any

    def __init__(self, table_name, conn=None, mapper=None):
        self._conn = conn
        self._mapper = mapper
        self._table_name = table_name
        self._where = WhereClause()
        self._select = SelectClause()
        self._one = False

    def one(self, conn=None):
        #: Return one instance of a model or raise an error.
        self._one = True

        return self

    def __await__(self):

        ctx = StatementContext()

        stmt = f'SELECT {self._select.__stmt__(ctx)} FROM "{self._table_name}"'

        if self._where:
            stmt = f"{stmt} WHERE {self._where.__stmt__(ctx)}"

        # Wait for the update.
        records = (yield from self._conn.fetch(stmt, *ctx.values).__await__())

        if callable(self._mapper):
            return self._mapper(records[0])

        return records[0]


class PartialInsert(ReturningMixin, ValuesMixin, PartialBase):
    """ Insert statement. """

    _table_name : str

    def __init__(self, table_name : str, conn=None, mapper=None):
        self._conn = conn
        self._table_name = table_name
        self._values = ValuesClause()
        self._returning = ReturningClause()
        self._mapper = mapper

    def __await__(self):

        ctx = StatementContext()

        stmt = f'INSERT INTO "{self._table_name}"'

        if self._values:
            stmt = f"{stmt} {self._values.__stmt__(ctx)}"

        if self.returning:
            stmt = f"{stmt} RETURNING ({self._returning.__stmt__(ctx)})"

        logger.debug(stmt)

        result = (yield from self._conn.fetchrow(stmt, *ctx.values).__await__())

        if callable(self._mapper):
            return self._mapper(result)

        return result


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
