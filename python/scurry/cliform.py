"""Edit forms in the CLI."""

import abc
import typing

ValueType = typing.TypeVar("ValueType")


class Value(abc.ABC, typing.Generic[ValueType]):
    def __init__(self, default: ValueType = None):
        self.current_value: typing.Optional[ValueType] = default
        return

    @abc.abstractmethod
    def parse(self, item: typing.Any) -> FieldType:
        raise NotImplementedError("not implemented")

    @abc.abstractmethod 
    def marshal(self) -> typing.Union[str,int,bool,float]:
        return ""
    
    
    def value(self) -> FieldType:
        return self.current_value
    
    def set_value(self, new_value: FieldType):
        self.current_value = new_value


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

ValidatorType = typing.Callable[[ValueType], None]

class Field(typing.Generic[ValueType]):
    def __init__(self, value: Value[ValueType], required=False, validators: typing.List[ValidatorType]=[]):
        self.validators = validators
        self.required = required
        self.value = value

    def parse(self, new_value: typing.Any):
        new_value = self.value.parse(new_value)
        self.value.parse()
        return
    
    def value(self) -> ValueType:
        return self.value.value()
    
    def validate(self):
        self.value.validate(self.value.value())
    

class Form:
    def __init__(self):
        return

    def marshal_form(self) -> typing.Dict[str, typing.Any]:
        return {}


class MyForm:
    my_field = Field()
