from scurry.structio.loader import Loader
from scurry.structio.field import String


def test_load():
    class MyConfig(Loader):
        my_field = String()

    conf = MyConfig()

    conf.load_object({"my_field": "my_value"})

    assert conf.my_field.value == "my_value"