# Basisklasse für alle Tabellen
# miniorm/models.py


from miniorm.db import get_connection
from miniorm.fields import Field


class Model:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._fields = {}

        for name, value in vars(cls).items():
            if isinstance(value, Field):
                cls._fields[name] = value

    def __init__(self, **kwargs):
        self.id = None
        for name, value in kwargs.items():
            if name not in self._fields:
                raise TypeError(f"{name} taucht nicht im Objekt auf.")
            # print(name, value)
            setattr(self, name, value)

    def __repr__(self):
        felder = ", ".join(f"{name}={getattr(self,name)!r}" for name in self._fields)

        return f"{self.__class__.__name__}({felder})"

    @classmethod
    def create_table_sql(cls):
        columns = []

        for name, field in cls._fields.items():
            columns.append(f"{name} {field.sql_type()}")

        columns = ", ".join(columns)

        sql = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})"
        return sql

    @classmethod
    def create_table(cls):
        conn = get_connection()
        conn.execute(cls.create_table_sql())
        conn.commit()

    def _insert_sql(self):
        werte = []

        names = list(self._fields)
        names = ", ".join(names)

        for name in self._fields:
            werte.append(getattr(self, name))

        placeholder = ", ".join("?" for _ in self._fields)

        sql = f"INSERT INTO {self.__class__.__name__.lower()} ({names}) VALUES ({placeholder})"

        return sql, werte

    def _insert(self):
        sql, werte = self._insert_sql()
        conn = get_connection()
        cursor = conn.execute(sql, werte)
        conn.commit()
        self.id = cursor.lastrowid

    def _update_sql(self):

        assignment = ", ".join(f"{name} = ?" for name in self._fields)
        sql = f"UPDATE {self.__class__.__name__.lower()} SET {assignment} WHERE id = ?"

        werte = [getattr(self, name) for name in self._fields]
        werte.append(self.id)
        return sql, werte

    def _update(self):
        sql, werte = self._update_sql()
        conn = get_connection()
        conn.execute(sql, werte)
        conn.commit()

    def save(self):
        if self.id is None:
            self._insert()
        else:
            self._update()
