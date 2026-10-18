# tests/test_fields.py
import pytest

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
    assert User.create_table() == (
        "CREATE TABLE IF NOT EXISTS user "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(20), age INTEGER)"
    )
