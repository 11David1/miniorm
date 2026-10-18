class Field:

    def __init__(self):
        pass

    def __set_name__(self, owner, name):
        self.name = name  # name = age # Owner = u
        self.internale_name = "_" + name  # _name

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.internale_name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.internale_name)

    def validate(self, value):
        if value is None:
            raise ValueError(f"{self.name} darf nicht None sein")

    def sql_type(self):
        raise NotImplementedError


class IntegerField(Field):

    def validate(self, value):
        super().validate(value)
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"Erwartet Integer, bekam {type(value)}")

    def sql_type(self):
        return "INTEGER"


class FloatField(Field):
    def validate(self, value):
        super().validate(value)
        if isinstance(value, bool) or not isinstance(value, float):
            raise TypeError(f"Erwartet Integer, bekam {type(value)}")

    def sql_type(
        self,
    ):
        return "FLOAT"


class CharField(Field):
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, str):
            raise TypeError(f"Erwartet String, bekam {type(value)}")
        if len(value) > self.max_length:
            raise ValueError("Text ist zu lang.")

    def sql_type(self):
        return f"VARCHAR({self.max_length})"
