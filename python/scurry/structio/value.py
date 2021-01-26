"""value contains all of the Value fields for structio"""

import abc
import typing

ValueType = typing.TypeVar("ValueType")


class Value(abc.ABC, typing.Generic[ValueType]):
    """Value is a generic field value."""

    value = None  # type: typing.Optional[ValueType]
    """The value.  It's type is generic"""

    @abc.abstractmethod
    def parse(self, value: typing.Any):
        """Parse the provided value, throwing exceptions if it is invalid."""
        return

    def validate(self):
        """Validate the provided value, throwing exceptions if it is invalid."""
        return


class String(Value[str]):
    """String is a `Value` field containing strings."""

    def __init__(self, default: typing.Optional[str] = None):
        """
        Create a new String.

        ---
        **Keywords:**
        * default (typing.Optional[str]): The default value for the field.

        """
        self.value = default

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


class Integer(Value[int]):
    """Integer is a `Value` field containing strings."""

    def __init__(self, default: typing.Optional[int] = None):
        """
        Create a new Integer.

        ---
        **Keywords**
        * default (typing.Optional[int]): The default value for this field.

        """
        self.value = default

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
