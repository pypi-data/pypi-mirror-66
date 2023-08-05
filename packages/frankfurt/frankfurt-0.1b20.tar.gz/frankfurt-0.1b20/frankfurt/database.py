from typing import Tuple, Type, Dict, Any, Optional

from contextvars import ContextVar

import asyncpg

from .models import BaseModel
from .fields import ForeignKeyField, BaseField, Action

from . import sql


class Meta:
    abstract : bool = False
    name: str
    table_name : str
    fields : Dict[str, BaseField] = {}
    db: Any

    def __init__(self, name : str):
        self.name = name
        self.table_name = name.lower()
        self.fields = {}

    @property
    def depends(self):
        # Return a list of methods that should be created first.

        deps = []

        for field in self.fields.values():
            if isinstance(field, ForeignKeyField):
                deps.append(field.to_field.model)

        return deps

    def extend_from_model(self, Meta):

        # Set the db.
        if hasattr(Meta, 'db'):
            self.db = Meta.db

        # Change the abstract.
        self.abstract = getattr(Meta, "abstract", self.abstract)

        # Change the table name.
        if hasattr(Meta, 'table_name'):
            self.table_name = Meta.table_name

    def __repr__(self):
        return "<MetaInfo for='{}' fields={} />".format(
            self.name,
            str(self.fields)
        )


class ModelType(type):

    def __new__(cls, name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):

        # Start with a fresh meta.
        meta = Meta(name)

        # Extract some information from bases.
        for base in bases:
            if hasattr(base, '_meta'):

                # Copy the reference to a database.
                meta.db = base._meta.db

                # Copy fields.
                for field_name, field in base._meta.fields.items():
                    meta.fields[field_name] = field.copy()

        if "Meta" in attrs:
            meta.extend_from_model(attrs["Meta"])

        # Append the fields defined in the model.
        for name, value in attrs.items():
            if isinstance(value, BaseField):
                meta.fields[name] = value

        # Append the meta information to the class.
        attrs["_meta"] = meta

        model = super().__new__(cls, name, bases, attrs)

        # Add the model to the dictionary of models if is not abstract.
        if not meta.abstract:
            meta.db.models[meta.table_name] = model

        # Add a reference for the fields.
        for field in meta.fields.values():
            field.model = model

        return model

    def from_record(cls, record):
        return cls(**record)


class RecordToModel:
    def __init__(self, awaitable, model):
        self._awaitable = awaitable
        self._model = model

    def __await__(self):

        # Wait for the result or results.
        result = (yield from self._awaitable.__await__())

        if isinstance(result, list):
            return (yield from map(self._model, result))
        else:
            return self._model(result)


class Database:
    """ Database instance to interact with asyncpg.
    """

    #: Keep track of all the models defined in this database.
    models: Dict[str, Type[BaseModel]]

    _model_class : Type[BaseModel]
    debug : bool = False

    pool : Any

    # Keep track of a connection.
    _conn = ContextVar('conn', default=None)

    def __init__(self, debug=False):

        self.models = {}

        # Declare the base model class.
        self._model_class = ModelType('Model', (BaseModel, ), {
            'Meta': type('Meta', (), {
                'abstract': True,
                'db': self
            })
        })

    @property
    def Model(self):
        return self._model_class

    @property
    def Connection(self):
        return self._connection_class

    async def create_pool(self, url : str, **kwargs):
        # Create a connection pool using asyncpg.
        self.pool = await asyncpg.create_pool(url, **kwargs)

    async def acquire(self):
        self._conn.set(await self.pool.acquire())
        return self._conn.get()

    async def release(self):
        if self._conn.get() is not None:
            await self.pool.release(self._conn.get())
            self._conn.set(None)

    def transaction(self):
        return self._conn.get().transaction()

    async def create_all_tables(self, conn=None):

        if conn is None:
            conn = self._conn.get()

        # Sort the models in the right order.
        models_unsorted = list(self.models.keys())
        models_sorted = []

        while len(models_unsorted) > 0:
            key = models_unsorted[0]
            deps = self.models[key]._meta.depends
            if all(_._meta.table_name in models_sorted for _ in deps):
                models_sorted.append(models_unsorted.pop(0))
            else:
                models_unsorted.append(models_unsorted.pop(0))

        # Run all the statements inside a transaction.
        async with conn.transaction():
            for table_name in models_sorted:
                await self.create_table(table_name, conn=conn)

    async def create_table(self, table_name, conn=None):

        if conn is None:
            conn = self._conn.get()

        if isinstance(table_name, ModelType):
            table_name = table_name._meta.table_name

        # Get the model.
        model = self.models[table_name]

        # Columns
        columns = []

        for field_name, field in model._meta.fields.items():

            # Resolve the constraint.
            constraint = sql.ColumnConstraint(
                not_null=field.not_null,
                unique=field.unique,
                primary_key=field.primary_key
            )

            # Resolve any dependecies.
            if isinstance(field, ForeignKeyField):
                reftable, refcolumn = field.refs()

                # Get the on_delete action.
                on_delete = None
                if isinstance(field.on_delete, Action):
                    on_delete = field.on_delete.value

                references = sql.ColumnConstraintReference(
                    reftable, refcolumn=refcolumn,
                    on_delete=on_delete
                )

                constraint.references = references

            # Append a new column.
            columns.append(sql.Column(
                field_name, field.__postgresql_type__(), constraint
            ))

        # CreateTable.
        stmt = sql.CreateTable(table_name, columns)
        return await stmt.execute(conn)

    def select(self, model, conn=None):

        if conn is None:
            conn = self._conn.get()

        return sql.PartialSelect(
            model._meta.table_name,
            mapper=lambda _: model(**_),
            conn=conn
        ).select(*list(model._meta.fields.keys()))

    def delete(self, model, conn=None):

        if conn is None:
            conn = self._conn.get()

        # Find a where clause.
        where_clause = sql.WhereClause()

        # Find a pk.
        for name, field in model._meta.fields.items():
            if name in model._data and field.primary_key:
                where_clause &= {name: model._data[name]}

        if not where_clause:
            raise Exception("Instance has no primary key.")

        # Create the delete statement.
        stmt = sql.PartialDelete(
            model._meta.table_name,
            conn=conn,
            mapper=lambda x: model(**x)
        )
        stmt.where(where_clause)
        stmt.returning(*model._meta.fields.keys())

        return stmt

    async def save(self, model, conn=None):

        if conn is None:
            conn = self._conn.get()

        # Update with values.
        values = {}

        # Find a where clause.
        where_clause = sql.WhereClause()

        # Find our pk.
        for name, field in model._meta.fields.items():
            if name in model._data and field.primary_key:
                where_clause &= {name: model._data[name]}
            elif name in model._data:
                values[name] = model._data[name]
            elif name in model._data_default:
                values[name] = model._data_default[name]

        if where_clause:

            # Create an update.
            stmt = sql.PartialUpdate(
                model._meta.table_name, conn=conn
            ).where(
                where_clause
            )

        else:

            # Insert statement
            stmt = sql.PartialInsert(
                table_name=model._meta.table_name,
                conn = conn
            )

        # Update the rest.
        stmt.values(**values)

        stmt.returning(*model._meta.fields.keys())

        model._update_from_record(await stmt)

        return model
