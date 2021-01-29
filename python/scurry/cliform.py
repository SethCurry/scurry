"""Edit forms in the CLI."""

import typing

ValueType = typing.TypeVar("ValueType")


class Value(typing.Generic[ValueType]):
    def __init__(self, default: ValueType = None, include_in_marshal: bool = True):
        self.value: typing.Optional[ValueType] = default
        return

    def validate(self, item: FieldType):
        return

    def parse(self, item: typing.Any) -> FieldType:
        raise NotImplementedError("not implemented")


class String(Field[str]):
    def parse(self, item: typing.Any) -> str:
        if type(item) == str:
            return item
        raise TypeError("expected a string")


class Integer(Field[int]):
    def parse(self, item: typing.Any) -> int:
        if type(item) == int:
            return item
        elif type(item) == str:
            return int(item)
        raise TypeError(
            "expected an integer, or a string that can be converted to integer"
        )


class Form:
    def __init__(self):
        return

    def marshal_form(self) -> typing.Dict[str, typing.Any]:
        return {}


class MyForm:
    my_field = Field()
