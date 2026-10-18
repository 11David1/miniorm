# Basisklasse für alle Tabellen
# miniorm/models.py
from miniorm.fields import Field


class Model:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._fields = {}

        for name, value in vars(cls).items():
            if isinstance(value, Field):
                cls._fields[name] = value

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if name not in self._fields:
                raise TypeError(f"{name} taucht nicht im Objekt auf.")
            # print(name, value)
            setattr(self, name, value)

    def __repr__(self):
        felder = ", ".join(f"{name}={getattr(self,name)!r}" for name in self._fields)

        return f"{self.__class__.__name__}({felder})"

    @classmethod
    def create_table(cls):

        columns = []

        for name, field in cls._fields.items():
            columns.append(f"{name} {field.sql_type()}")

        columns = ", ".join(columns)

        sql = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})"
        return sql
