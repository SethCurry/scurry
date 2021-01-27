from scurry.structio import Integer, String, ValidationError


def test_validate():
    def validator(in_str: str):
        if in_str != "my_test":
            raise ValidationError

    my_field = String(validator=validator)

    my_field.parse("not_my_test")
    try:
        my_field.validate()
        raise TypeError("validation should have failed")
    except ValidationError:
        pass
