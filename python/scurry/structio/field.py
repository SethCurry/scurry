"""value contains all of the Value fields for structio"""

import abc
import typing

FieldType = typing.TypeVar("FieldType")
ValidatorType = typing.Callable[[FieldType], None]


class ValidationError(Exception):
    """Base validation exception class."""

    pass


class Field(abc.ABC, typing.Generic[FieldType]):
    """Field is a generic field value."""

    value = None  # type: typing.Optional[FieldType]
    """The value.  It's type is generic"""

    def __init__(
        self,
        default: typing.Optional[FieldType] = None,
        validator: ValidatorType = None,
    ):
        self.value = default
        self.validator = validator

    @abc.abstractmethod
    def parse(self, value: typing.Any):
        """Parse the provided value, throwing exceptions if it is invalid."""
        return

    def validate(self):
        """Validate the current value."""
        if self.validator is not None:
            self.validator(self.value)


class String(Field[str]):
    """String is a `Field` containing  a string."""

    def parse(self, value: typing.Any):
        """
        Parse the provided value if possible.

        ---
        **Arguments:**
        * value (typing.Any): The value to be parsed.

        """
        if type(value) != str:
            raise ValueError("value must be a string")

        self.value = value


class Integer(Field[int]):
    """Integer is a `Field` containing strings."""

    def parse(self, value: typing.Any):
        """
        Parse the provided value if possible.

        ---
        **Arguments:**
        * value (typing.Any): The value to be parsed.

        """
        if type(value) != int:
            raise ValueError("value must be an int")

        self.value = value
