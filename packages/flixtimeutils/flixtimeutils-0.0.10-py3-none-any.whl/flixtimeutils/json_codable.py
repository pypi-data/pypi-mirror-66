import json

from enum import Enum


class ParsingStyle(Enum):
    SNAKE_CASE = 1
    CAMEL_CASE = 2


class JSONEncodable:

    def to_dictionary(self, style: ParsingStyle) -> dict:
        if style == ParsingStyle.SNAKE_CASE:
            return self.__dict__
        else:
            dictionary = {}
            for key in self.__dict__.keys():
                value = self.__dict__[key]
                camel_case_key = JSONEncodable.to_camel_case(key)
                dictionary[camel_case_key] = value
            return dictionary

    def to_json(self, style: ParsingStyle) -> str:
        return json.dumps(self, default=lambda o: o.to_dictionary(style=style),
                          sort_keys=True, indent=4)

    @classmethod
    def to_camel_case(cls, snake_case_value: str) -> str:
        components = snake_case_value.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])


class JSONCodable(JSONEncodable):
    """
    A class representing an object that can be parsed from a JSON dictionary. Overriding the parsing_keys property
    allows easy mapping from the JSON dictionary keys to the objects properties.
    For example having:

    parsing_keys = {
        "name": "title"
    }

    will store the value from the JSON dictionary key "name" in the object's title property.

    Attributes
    ----------
    parsing_keys : dict
        The keys to map from JSON to object properties
    """
    parsing_keys = {}

    def __init__(self, **entries):
        for entry_key, value in entries.items():
            # Check if another key is specified in parsing keys, else fall back on the entry_key value
            key = self.parsing_keys.get(entry_key, entry_key)

            try:
                # Make sure the property name exists, else skip the value
                getattr(self, key)

                # Set the value for entry_key as property on self
                setattr(self, key, value)
            except AttributeError:
                # getattr raised an AttributeError, continue with the next value
                continue
