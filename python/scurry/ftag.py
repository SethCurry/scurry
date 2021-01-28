"""Manage tags in file names."""

import typing


class Attributes:
    """
    A collection of attributes for a file.

    ---
    **Properties:**
    * tags (typing.List[str]): The tags that are on the file.
    * fields (typing.Dict[str,str]): The key-value fields on the file.

    """

    def __init__(self):
        """Create a new `Attributes` object."""
        self.tags: typing.List[str] = []
        self.fields: typing.Dict[str, str] = {}

    def has(self, name: str) -> bool:
        """
        Determine whether the given name exists as a tag or field on this file.

        ---
        **Arguments**:
        * name (str): The name of the tag or field

        ---
        **Returns:** bool indicating whether the name exists as a tag or field

        """
        if name in self.tags or name in self.fields:
            return True
        return False

    def __str__(self) -> str:
        """Convert these Attributes back into a string to use in a file name."""
        if len(self.tags) == 0 and len(self.fields) == 0:
            return ""

        ret = "["
        ret = ret + " ".join(self.tags)
        if len(self.fields.keys()) > 0:
            for key, val in self.fields.items():
                ret = ret + " " + key + "=" + val
        ret = ret + "]"

        return ret


def parse_filename(name: str) -> Attributes:
    """
    Parse the tags and attributes from the provided file name.

    ---
    **Arguments:**
    * name (str): The name of the file, can be either an absolute path or just the file name.
    """

    ret = Attributes()
    in_tag = False
    is_field = False
    field_value = ""
    tag_name = ""

    for c in name:
        if c == "[":
            in_tag = True
            continue
        elif c == "]":
            in_tag = False
            if is_field:
                ret.fields[tag_name] = field_value
            else:
                ret.tags.append(tag_name)
            tag_name = ""
            field_value = ""
            is_field = False
            continue
        elif c == "=" and in_tag:
            is_field = True
            continue
        elif c == " " and in_tag:
            if is_field:
                ret.fields[tag_name] = field_value
            else:
                ret.tags.append(tag_name)
            tag_name = ""
            field_value = ""
            is_field = False
            continue

        if in_tag and is_field:
            field_value = field_value + c
            continue
        elif in_tag:
            tag_name = tag_name + c
            continue

    return ret


def walk(root: str) -> typing.Dict[str, Attributes]:
    # TODO implement the walk function
    # TODO change this to a generator
    return {}