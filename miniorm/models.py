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
            setattr(self, name, value)
