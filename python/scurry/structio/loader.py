"""Loader defines the class that actually loads the config."""

import typing
from scurry.structio.field import Field


class Loader:
    """
    Load data from arbitrary sources.

    Typically used as a parent class, where you define your own
    data classes like this:

    ```
    class MyConfig(dataloader.Loader):
        my_field = dataloader.Field(dataloader.String())
    ```
    """

    def __init__(self):
        """Create a new Loader."""
        return

    def __iter__(self):
        for prop, val in vars(self):
            if isinstance(val, Field):
                yield (prop, val)

    def __get_field(self, name: str) -> Field:
        try:
            attr = getattr(self, name)
        except AttributeError:
            cls_attr = getattr(self.__class__, name)
            attr = cls_attr()
            self.__dict__[name] = attr

        if not isinstance(attr, Field):
            raise TypeError

        return attr

    def load_object(self, obj: typing.Dict[str, typing.Any]):
        """
        Load the given object into this Loader.

        ---
        **Arguments:**
        * obj (typing.Any): The data (typically a dictionary) to be loaded.

        """
        for key, val in obj.items():
            self.__get_field(key).parse(val)
