# tests/test_fields.py
import pytest

from miniorm.fields import CharField, IntegerField


class Dummy:
    age = IntegerField()
    name = CharField(max_length=5)


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
