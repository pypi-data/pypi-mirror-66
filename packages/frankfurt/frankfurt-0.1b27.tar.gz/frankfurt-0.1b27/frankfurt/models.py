from typing import Tuple, Type, Dict, Any, List

import asyncpg

from frankfurt.fields import BaseField, ForeignKeyField, Action


class BaseModel:
    def __init__(self, **kwargs):

        # Save the value of the fields in this dict
        self._data_default = {}
        self._data = {}

        # Check for the kwargs in the fields.
        for name, value in kwargs.items():
            self._set_data(name, value)

        # Continue with default values.
        for name, field in self._meta.fields.items():
            if name not in self._data:
                if field.has_default:
                    self._set_data_default(name, field.default)

        # Check for not nulls (or maybe types?)
        for name, field in self._meta.fields.items():
            msg = f"Field {name} cannot be null (None)"

            if name in self._data:
                if field.not_null and self._data[name] is None:
                    raise TypeError(msg)
            elif name in self._data_default:
                if field.not_null and self._data_default[name] is None:
                    raise TypeError(msg)

    def _set_data(self, name, value):
        if name not in self._meta.fields:
            raise TypeError(f"Model has no field {name}.")

        # Assert the type for this field.
        try:
            self._meta.fields[name].assert_type(value)
            self._data[name] = value
        except TypeError as e:
            msg = f"Field {name} can't accept value {value}: {str(e).lower()}"
            raise TypeError(msg)

    def _set_data_default(self, name, value):
        try:
            self._meta.fields[name].assert_type(value)
            self._data_default[name] = value
        except TypeError as e:
            msg = f"Field {name} can't accept value {value}: {str(e).lower()}"
            raise TypeError(msg)

    def __setitem__(self, key : str, value):
        if key not in self._meta.fields:
            msg = "Model {} has not field {}.".format(self._meta.name, key)
            raise KeyError(msg)

        self._data[key] = value

        if key in self._data_default:
            del self._data_default[key]

    def __getitem__(self, key : str):
        if key not in self._meta.fields:
            msg = "Model {} has not field {}.".format(self._meta.name, key)
            raise KeyError(msg)

        if key in self._data:
            return self._data[key]

        if key in self._data_default:
            return self._data_default[key]

        raise KeyError("Field {} has no value.".format(key))

    def _update_from_record(self, record):
        for name, value in record.items():
            if name in self._meta.fields:
                self._data[name] = value

                if name in self._data_default:
                    del self._data_default[name]

    async def save(self, conn=None):
        await self._meta.db.save(self, conn=conn)

    async def delete(self, conn=None):
        await self._meta.db.delete(self, conn=conn)
