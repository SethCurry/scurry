"""field stores all the Field objects."""

import typing
from scurry.structio.value import Value

FieldType = typing.TypeVar("FieldType")
FieldValidateType = typing.Callable[[FieldType], None]


class Field(typing.Generic[FieldType]):
    """Field a single field within a `Loader`."""

    def __init__(
        self,
        value_type: Value[FieldType],
        validator: typing.Optional[FieldValidateType] = None,
    ):
        """
        Create a new Field.

        ---
        **Arguments:**
        * value_type (Value): The `Value` to use to parse and validate.

        ---
        **Keywords**:
        * validator (FieldValidateType): The function to use to validate parsed values.

        """
        self.validator = validator
        self.value_type = value_type

    def parse(self, value: typing.Any):
        """
        Parse a value using the contained field.

        ---
        **Arguments**:
        * value (typing.Any): The value to be parsed.

        """
        self.value_type.parse(value)

    def value(self) -> typing.Optional[FieldType]:
        """Get the value of the contained `Value`."""
        return self.value_type.value

    def validate(self):
        """Call the `validator` function if one was supplied."""
        if self.validator is not None:
            self.validator(self.value_type.value())
        return
