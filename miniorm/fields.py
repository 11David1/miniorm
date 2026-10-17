class Field:

    def __init__(self):
        pass

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 0)

    def validate(self, value):
        if value is None:
            raise ValueError(f"{self.name} darf nicht None sein")


class IntegerField(Field):

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Erwartet Integer, bekam {type(value)}")


class FloatField(Field):

    def validate(self, value):
        if not isinstance(value, float):
            raise TypeError(f"Erwartet Float, bekam {type(value)}")


class CharField(Field):

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Erwartet String, bekam {type(value)}")
