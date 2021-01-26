from scurry.structio.field import Field
from scurry.structio.value import String


def test_parse():
    my_field = Field(String())

    my_field.parse("my_string")

    assert my_field.value() == "my_string"
