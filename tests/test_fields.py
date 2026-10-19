# tests/test_fields.py
import pytest

from miniorm.db import connect
from miniorm.fields import CharField, IntegerField
from miniorm.models import Model


class Dummy:
    age = IntegerField()
    name = CharField(max_length=5)


class User(Model):
    name = CharField(max_length=20)
    age = IntegerField()


def test_stores_value_per_instance():
    a, b = Dummy(), Dummy()
    a.age = 1
    b.age = 2
    assert a.age == 1 and b.age == 2


def test_rejects_wrong_type():
    with pytest.raises(TypeError):
        Dummy().age = "zehn"


def test_max_length():
    with pytest.raises(ValueError):
        Dummy().name = "zu lang"


def test_field_knows_its_name():
    assert Dummy.__dict__["age"].name == "age"


def test_init_sets_values():
    u = User(name="David", age=19)
    assert u.name == "David" and u.age == 19


def test_init_validates():
    with pytest.raises(TypeError):
        User(age="zehn")


def test_init_rejects_unknown():
    with pytest.raises(TypeError):
        User(foo=1)


def test_repr():
    u = User(name="David", age=19)
    assert repr(u) == "User(name='David', age=19)"


def test_create_table():
    assert User.create_table_sql() == (
        "CREATE TABLE IF NOT EXISTS user "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(20), age INTEGER)"
    )


def test_save_inserts_and_sets_id():
    connect(":memory:")
    User.create_table()
    u = User(name="David", age=19)
    u.save()
    assert u.id == 1


def test_save_updates_instead_of_duplicating():
    conn = connect(":memory:")
    User.create_table()
    u = User(name="David", age=19)
    u.save()
    u.age = 20
    u.save()
    rows = conn.execute("SELECT id, name, age FROM user").fetchall()
    assert rows == [(1, "David", 20)]


def test_get():
    connect(":memory:")
    User.create_table()
    u = User(name="David", age=19)
    u.save()
    assert User.get(u.id).name == "David"
    assert User.get(999) is None


import pytest

from miniorm.fields import CharField, FloatField, IntegerField

# --- None-Handling ---------------------------------------------------


class Nullable:
    age = IntegerField()
    price = FloatField()
    name = CharField(max_length=5)


class Required:
    age = IntegerField(not_null=True)
    price = FloatField(not_null=True)
    name = CharField(max_length=5, not_null=True)


@pytest.mark.parametrize("attr", ["age", "price", "name"])
def test_none_allowed_by_default(attr):
    obj = Nullable()
    setattr(obj, attr, None)
    assert getattr(obj, attr) is None


@pytest.mark.parametrize("attr", ["age", "price", "name"])
def test_none_rejected_when_not_null(attr):
    obj = Required()
    with pytest.raises(ValueError):
        setattr(obj, attr, None)


def test_type_check_still_works_with_constraints():
    with pytest.raises(TypeError):
        Required().age = "zehn"


def test_max_length_still_works_with_constraints():
    with pytest.raises(ValueError):
        Required().name = "zu lang"


# --- Constraints werden gespeichert ----------------------------------


def test_constraints_are_stored():
    f = CharField(max_length=10, not_null=True, unique=True, default="x")
    assert f.max_length == 10
    assert f.not_null is True
    assert f.unique is True
    assert f.default == "x"


def test_constraint_defaults():
    f = IntegerField()
    assert f.not_null is False
    assert f.unique is False
    assert f.default is None


# --- column_sql ------------------------------------------------------


def test_column_sql_plain():
    assert IntegerField().column_sql() == "INTEGER"


def test_column_sql_not_null():
    assert IntegerField(not_null=True).column_sql() == "INTEGER NOT NULL"


def test_column_sql_unique():
    assert CharField(max_length=20, unique=True).column_sql() == "VARCHAR(20) UNIQUE"


def test_column_sql_default_number():
    assert IntegerField(default=0).column_sql() == "INTEGER DEFAULT 0"


def test_column_sql_all_constraints():
    f = IntegerField(not_null=True, unique=True, default=0)
    assert f.column_sql() == "INTEGER DEFAULT 0 NOT NULL UNIQUE"


# @pytest.mark.xfail(reason="String-Defaults brauchen noch Anführungszeichen")
def test_column_sql_default_string():
    f = CharField(max_length=10, default="unbekannt")
    assert f.column_sql() == "VARCHAR(10) DEFAULT 'unbekannt'"


def test_column_sql_default_with_quote():
    f = CharField(max_length=20, default="O'Brien")
    assert f.column_sql() == "VARCHAR(20) DEFAULT 'O''Brien'"
