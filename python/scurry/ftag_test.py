"""Test the scurry.ftag module."""

from scurry.ftag import parse_filename


def test_parse_filename():
    fname = "MyFile [tag afield=avalue]"

    attributes = parse_filename(fname)

    assert attributes.tags == ["tag"]
    assert attributes.fields == {"afield": "avalue"}


def test_parse_double_equals():
    fname = "MyFile [afield==avalue]"

    try:
        attributes = parse_filename(fname)
        raise Exception("should have failed to parse")
    except Exception:
        # TODO this should be a more specific exception
        pass


def test_parse_equals_space():
    fname = "MyFile [afield=]"

    try:
        attributes = parse_filename(fname)
        raise Exception("should have failed to parse")
    except Exception:
        # TODO this should be a more specific exception
        pass

def test_Attribute_str_multi_key_multi_tag():
    # TODO write this test
